from bs4 import BeautifulSoup
import requests
from article import Article
import datetime
import streamlit as st


def search(end_date: datetime.date):
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

            print(headline)
            print(date)

            # Jun. 28, 2022
            date = datetime.datetime.strptime(date, '%b. %d, %Y')
            article_objects.append(Article(headline, url, date, category, text))
            if date.date() < end_date:
                finished = True
                break

    return article_objects


if __name__ == '__main__':
    search(datetime.datetime.strptime('09/07/2022', '%d/%m/%Y').date())
