from bs4 import BeautifulSoup
import requests
from article import Article
import datetime
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
            soup = BeautifulSoup(html, 'html5lib')

            date = soup.find('span', class_='date')
            if date == '':
                self.date = datetime.datetime.strptime(date.text, '%d/%m/%Y %H:%M:%S')

            content = date.find_parent().__str__().replace('/ HaitiLibre', '/ iciHaiti', 1).split('/ iciHaiti')[0].split('</table>')[-1]
            self._full_article = content[:-3].strip()

        return check_text(self._full_article)


def haiti_libre_search(end_date: datetime.date, max_num: int = 10000):
    finished = False
    article_objects = []
    page_number = 0

    while not finished:
        page_number += 1
        url = f'https://www.haitilibre.com/en/flash-infos-en-{page_number}.html'

        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')

        articles = soup.find_all('span', class_='titre16color')

        for i, a in enumerate(articles):
            headline = a.find_parents(limit=3)[2].find_all('td', class_='text')[0].find('span', class_='titre16color').text
            text = a.find_parents(limit=3)[2].find_all('td', class_='text')[1].text
            url = a.find_parents(limit=3)[2].find_all('td', class_='text')[-1].find('a')['href']
            date = a.fetchNextSiblings()[1].text
            categories = ['Haite Libre'] if not 'iciHaiti' in headline else ['iciHaiti']
            try:
                categories.append(headline.split(' - ')[1].split(':')[0].strip())
                headline = headline.split(' - ')[1].split(':')[1].strip()
            except IndexError:
                pass

            if date != '':
                date = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
                if date.date() < end_date or i >= max_num:
                    finished = True
                    break
                article_objects.append(HaitiLibreArticle(headline, url, date, categories, text))

            else:
                try:
                    date = article_objects[-1].date
                except IndexError:
                    continue

                article_objects.append(HaitiLibreArticle(headline, url, date, categories, text))
    return article_objects


if __name__ == '__main__':
    arts = haiti_libre_search(datetime.date(2023, 1, 2), 20)
