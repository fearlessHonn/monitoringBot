from haitian_times import haitian_times_search
from haiti_libre import haiti_libre_search
import datetime


def search(end_date: datetime.date):
    haitian_times_articles = haitian_times_search(end_date)
    haiti_libre_articles = haiti_libre_search(end_date)

    all_articles = haitian_times_articles + haiti_libre_articles
    return sort_articles(all_articles)


def sort_articles(articles: list):
    articles.sort(key=lambda x: x.date, reverse=True)
    return articles


if __name__ == '__main__':
    search(datetime.datetime.strptime('09/07/2022', '%d/%m/%Y').date())
