from bs4 import BeautifulSoup
import requests
from article import Article
import datetime
import streamlit as st
from text_checking import check_text


class HaitiLibreArticle(Article):
    def __init__(self, headline, url, date, category, text):
        super().__init__(headline, url, date, category, text)

        if 'https://' not in self.url:
            self.url = 'https://www.haitilibre.com' + self.url

        if self.text == 'Read more on iciHaiti.com...':
            self.text = ''

    @property
    def full_article(self):
        if self._full_article == 'N/A':
            html = requests.get(self.url).text
            soup = BeautifulSoup(html, 'html.parser')

            date = soup.find('span', class_='date')
            if date == '':
                self.date = datetime.datetime.strptime(date.text, '%d/%m/%Y %H:%M:%S')

            content = date.find_parent().__str__().replace('/ HaitiLibre', '/ iciHaiti', 1).split('/ iciHaiti')[0].split('</table>')[-1]
            self._full_article = content[:-3].strip()

        self.german_version.translate_full_article()
        return check_text(self._full_article)


@st.cache(allow_output_mutation=True)
def haiti_libre_search(end_date: datetime.date):
    finished = False
    article_objects = []
    page_number = 0

    while not finished:
        page_number += 1
        url = f'https://www.haitilibre.com/en/flash-infos-en-{page_number}.html'

        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        articles = soup.find_all('span', class_='titre16color')

        for a in articles:
            headline = a.find_parents(limit=3)[2].find_all('td', class_='text')[0].find('span', class_='titre16color').text
            text = a.find_parents(limit=3)[2].find_all('td', class_='text')[1].text
            url = a.find_parents(limit=3)[2].find_all('td', class_='text')[-1].find('a')['href']
            date = a.fetchNextSiblings()[1].text
            category = headline.split(' - ')[1].split(':')[0].strip()

            if date != '':
                date = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
                if date.date() < end_date:
                    finished = True
                    break
                article_objects.append(HaitiLibreArticle(headline, url, date, category, text))

            else:
                date = article_objects[-1].date
                article_objects.append(HaitiLibreArticle(headline, url, date, category, text))

    return article_objects


if __name__ == '__main__':
    arts = haiti_libre_search(datetime.date(2022, 7, 9))
    for a in arts:
        print(a.headline)
        b = a.full_article