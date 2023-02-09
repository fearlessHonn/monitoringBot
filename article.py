from text_checking import check_text


class Article:
    def __init__(self, headline, url, date, categories, text):
        self.headline = check_text(headline)
        self.url = url
        self.date = date
        self.text = check_text(text)
        self.categories = [check_text(category) for category in categories]

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