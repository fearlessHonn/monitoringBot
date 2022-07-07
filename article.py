class Article:
    def __init__(self, headline, url, date, text=''):
        self.headline = headline
        self.url = url
        self.date = date
        self.text = text

        if 'https://' not in self.url:
            self.url = 'https://www.haitilibre.com' + self.url

        if self.text == 'Read more on iciHaiti.com...':
            self.text = ''

    def __str__(self):
        return f'{self.headline} \n{self.text} \n{self.url} \n{self.date} \n\n'

    def to_html(self):
        return f"""<a href='{self.url}'><b>{self.headline}</b></a></br>
                    {self.text}{'</br>' if self.text != '' else ''}
                    {self.date.strftime('%d.%m.%Y')}</br></br></br>"""



