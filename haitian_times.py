from bs4 import BeautifulSoup
import requests
from article import Article
import datetime
import streamlit as st
from text_checking import check_text


class HaitianTimesArticle(Article):
    @property
    def full_article(self):
        if self._full_article == 'N/A':
            html = requests.get(self.url).text
            soup = BeautifulSoup(html, 'html.parser')

            self.category = soup.find('a', rel='category tag').text

            if 'To view the full story' in html:
                summary = soup.find('div', class_='article-summary')
                self._full_article = summary.find('p').text + ' (Overview)'

            else:
                content = soup.find('div', class_='entry-content')
                self._full_article = '\n'.join([para.text for para in content.find_all('p')])

        self.german_version.translate_full_article()
        return check_text(self._full_article)

@st.cache(allow_output_mutation=True)
def haitian_times_search(end_date: datetime.date):
    finished = False
    article_objects = []
    page_number = 0

    while not finished:
        page_number += 1
        url = f'https://haitiantimes.com/category/haiti/page/{page_number}/'

        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        articles = soup.find_all('div', class_='entry-container')

        for a in articles:
            headline = a.find('h2', class_='entry-title').text
            url = a.find('h2', class_='entry-title').find('a')['href']
            date = a.find('time', class_='entry-date published').text
            category = 'Haitian Times'
            text = ''

            date = datetime.datetime.strptime(date, '%b. %d, %Y')
            if date.date() < end_date:
                finished = True
                break

            article_objects.append(HaitianTimesArticle(headline, url, date, category, text))


    return article_objects
