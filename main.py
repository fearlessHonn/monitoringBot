import time
from podio_access import get_last_date, create_monitoring_entry, updated_status, delete_outdated_articles, get_config
from haiti_libre import haiti_libre_search
import datetime
from config import Settings


settings = Settings()
while True:
    if time.time() % (settings.refresh_interval * 60 * 60) <= 10 or 1:
        last_refresh = get_last_date()
        articles = haiti_libre_search(last_refresh.date())

        count = 0
        num_of_articles = len(articles)
        articles = sorted(articles, key=lambda x: x.date)
        for i, article in enumerate(articles):
            print(f'Processing article {i+1} of {num_of_articles}')
            if article.date >= (last_refresh + datetime.timedelta(seconds=59)):
                create_monitoring_entry(article.headline, article.date, article.full_article, article.url, article.categories, article.text)
                count += 1

        if settings.post_status_message:
            if count == 0:
                pass
            elif count == 1:
                updated_status(f"Es wurde 1 neuer Artikel hinzugefügt. Siehe \"Monitoring\"-App.")
            else:
                updated_status(f"Es wurden {count} neue Artikel hinzugefügt. Siehe \"Monitoring\"-App.")

        delete_outdated_articles()
        settings.write(*get_config())
        print('Finished update iteration')
