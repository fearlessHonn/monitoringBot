from bs4 import BeautifulSoup
import requests
from article import Article
import datetime
import streamlit as st
from text_checking import check_text


class HaitianTimesArticle(Article):
    def __init__(self, headline, url, date, categories, text):
        super().__init__(headline, url, date, categories, text)

    @property
    def full_article(self):
        if self._full_article == 'N/A':
            html = requests.get(self.url).text
            soup = BeautifulSoup(html, 'html5lib')

            self.categories.append(soup.find('a', rel='category tag').text)

            if 'To view the full story' in html:
                if summary := soup.find('div', class_='article-summary'):
                    self._full_article = summary.find('p').text + ' (Overview)'
                else:
                    self._full_article = 'Nicht verfügbar.'

            else:
                content = soup.find('div', class_='entry-content')
                self._full_article = '\n'.join([para.text for para in content.find_all('p')])

        return check_text(self._full_article)


def haitian_times_search(end_date: datetime.date, max_num: int = 1000):
    finished = False
    article_objects = []
    page_number = 0

    while not finished:
        page_number += 1
        url = f'https://haitiantimes.com/category/haiti/page/{page_number}/'

        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')

        articles = soup.find_all('div', class_='entry-container')

        for i, a in enumerate(articles):
            headline = a.find('h2', class_='entry-title').text
            url = a.find('h2', class_='entry-title').find('a')['href']
            date = a.find('time', class_='entry-date published').text
            categories = ['Haitian Times']
            text = ''

            date = datetime.datetime.strptime(date, '%b. %d, %Y')
            if date.date() < end_date or i >= max_num:
                finished = True
                break

            article_objects.append(HaitianTimesArticle(headline, url, date, categories, text))

    return article_objects


if __name__ == '__main__':
    print(len(haitian_times_search(datetime.date(2023, 1, 2))))