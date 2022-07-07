import requests
from bs4 import BeautifulSoup
from translate import translator


class Article:
    def __init__(self, headline, url, date, category, text=''):
        self.headline = headline
        self.url = url
        self.date = date
        self.text = text
        self.category = category

        self.german_version = GermanArticle(self.headline, self.url, self.date, self.category, self.text)

        if 'https://' not in self.url:
            self.url = 'https://www.haitilibre.com' + self.url

        if self.text == 'Read more on iciHaiti.com...':
            self.text = ''

        self._full_article = 'N/A'

    def __str__(self):
        return f'{self.headline} \n{self.text} \n{self.url} \n{self.date} \n\n'

    def to_html(self):
        if self.text != '':
            return f"""{self.date.strftime('%d.%m.%Y')}</br>
                    <a href='{self.url}'><b>{self.headline}</b></a></br>
                    {self.text}</br>"""
        else:
            return f"""{self.date.strftime('%d.%m.%Y')}</br>
                        <a href='{self.url}'><b>{self.headline}</b></a></br>"""

    @property
    def full_article(self):
        if self._full_article == 'N/A':
            html = requests.get(self.url).text
            soup = BeautifulSoup(html, 'html.parser')

            if 'libre' in self.url:
                full = soup.find('span', class_='date').find_parent()
                full = str(full).split('/ HaitiLibre')[0]
                full = full.split('</table>')[-1]
                self._full_article = full[:-3].strip()

            elif 'icihaiti' in self.url:
                full = soup.find('span', class_='date').find_parent()
                full = str(full).split('/ iciHaiti')[0]
                full = full.split('</table>')[-1]
                self._full_article = full[:-3].strip()

        return self._full_article


class GermanArticle:
    def __init__(self, headline, url, date, category, text=''):
        self.headline = headline
        self.url = url
        self.date = date
        self.text = text
        self.category = category

        self.to_german()

    def to_german(self):
        if self.text != '':
            self.text = translator.translate(self.text, dest='de').text

        self.headline = translator.translate(self.headline, dest='de').text

    def to_html(self):
        if self.text != '':
            return f"""{self.date.strftime('%d.%m.%Y')}</br>
                    <a href='{self.url}'><b>{self.headline}</b></a></br>
                    {self.text}</br>"""
        else:
            return f"""{self.date.strftime('%d.%m.%Y')}</br>
                        <a href='{self.url}'><b>{self.headline}</b></a></br>"""
