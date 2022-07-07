from translate import translator


class Article:
    def __init__(self, headline, url, date, category, text='', translate=False):
        self.headline = headline
        self.url = url
        self.date = date
        self.text = text
        self.category = category

        if 'https://' not in self.url:
            self.url = 'https://www.haitilibre.com' + self.url

        if self.text == 'Read more on iciHaiti.com...':
            self.text = ''

        if translate:
            self.to_german()

    def __str__(self):
        return f'{self.headline} \n{self.text} \n{self.url} \n{self.date} \n\n'

    def to_html(self):
        if self.text != '':
            return f"""{self.date.strftime('%d.%m.%Y')}</br>
                    <a href='{self.url}'><b>{self.headline}</b></a></br>
                    {self.text}</br>
                    </br></br>"""
        else:
            return f"""{self.date.strftime('%d.%m.%Y')}</br>
                        <a href='{self.url}'><b>{self.headline}</b></a></br>
                        </br></br>"""

    def to_german(self):
        if self.text != '':
            self.text = translator.translate(self.text, dest='de').text

        self.headline = translator.translate(self.headline, dest='de').text
