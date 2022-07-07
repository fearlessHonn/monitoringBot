from bs4 import BeautifulSoup
import requests
from article import Article
import datetime
import streamlit as st


@st.cache
def search(end_date: datetime.date):
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
            headline = a.find_parents(limit=3)[2].find_all('td', class_='text')[0].find('span').text
            text = a.find_parents(limit=3)[2].find_all('td', class_='text')[1].text
            url = a.find_parents(limit=3)[2].find_all('td', class_='text')[-1].find('a')['href']
            date = a.fetchNextSiblings()[1].text
            category = headline.split(' - ')[1].split(':')[0].strip()

            if date != '':
                date = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
                if category not in ['Sports', 'Diaspora Covid-19']:
                    article_objects.append(Article(headline, url, date, category, text))
                if date.date() < end_date:
                    finished = True
                    break
            else:
                date = article_objects[-1].date
                article_objects.append(Article(headline, url, date, text))

    return article_objects


"""if __name__ == '__main__':
    with open('output.html', 'w+') as file:
        output = '<html><body>\n'
        for art in article_objects:
            output += art.to_html()
        output += '</body></html>'

        file.write(output)"""


if __name__ == '__main__':
    arts = search(datetime.datetime.today().date())
    print(arts[0].url)
    arts[0].fetch_article()