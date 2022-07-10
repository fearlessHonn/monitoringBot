from translation import translator
from text_checking import check_text


class Article:
    def __init__(self, headline, url, date, category, text):
        self.headline = check_text(headline)
        self.url = url
        self.date = date
        self.text = check_text(text)
        self.category = check_text(category)

        self._german_version = None
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
        return self._full_article

    @property
    def german_version(self):
        if self._german_version is None:
            self._german_version = GermanArticle(self.headline, self.url, self.date, self.category, self.text, self)

        return self._german_version


class GermanArticle(Article):
    def __init__(self, headline, url, date, category, text, parent_article):
        super().__init__(headline, url, date, category, text)

        self.parent_article = parent_article

        t1, t2, t3 = translator.translate([self.headline, self.category, self.text], dest='de')
        self.headline, self.category, self.text = t1.text, t2.text, t3.text

        if self._full_article != 'N/A':
            self.translate_full_article()

    def translate_full_article(self):
        self._full_article = translator.translate(self._full_article, dest='de').text

    @property
    def full_article(self):
        if self._full_article == 'N/A':
            self._full_article = self.parent_article.full_article
            self.translate_full_article()

        return self._full_article
