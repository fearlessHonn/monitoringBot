from translate import translator


class Article:
    def __init__(self, headline, url, date, text='', translate=False):
        self.headline = headline
        self.url = url
        self.date = date
        self.text = text

        if 'https://' not in self.url:
            self.url = 'https://www.haitilibre.com' + self.url

        if self.text == 'Read more on iciHaiti.com...':
            self.text = ''

        if translate:
            self.to_german()

    def __str__(self):
        return f'{self.headline} \n{self.text} \n{self.url} \n{self.date} \n\n'

    def to_html(self):
        return f"""<a href='{self.url}'><b>{self.headline}</b></a></br>
                    {self.text}{'</br>' if self.text != '' else ''}
                    {self.date.strftime('%d.%m.%Y')}</br></br></br>"""

    def to_german(self):
        if self.text != '':
            self.text = translator.translate(self.text, dest='de').text

        self.headline = translator.translate(self.headline, dest='de').text
