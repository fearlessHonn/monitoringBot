from podio import auth
from datetime import datetime, timedelta
import os
from config import Settings
import re

client_secret = os.environ.get("PODIO_CLIENT_SECRET")
client_id = "haiti-news-scraper"
app_id = 28278401
space_id = 2830461
app_token = "79ae827be829a3f8ee7d7fbcdcba7896"  # os.environ.get("PODIO_MONITORING_APP_TOKEN_HAITI")
PODIO_PASSWORD = os.environ.get("PODIO_PASSWORD")
PODIO_EMAIL = os.environ.get("PODIO_EMAIL")

settings = Settings()

if client_secret is None:
    print("Please set the environment variable PODIO_CLIENT_SECRET")
    exit(1)
if app_token is None:
    print("Please set the environment variable PODIO_MONITORING_APP_TOKEN")
    exit(1)


def create_monitoring_entry(title: str, date: datetime, content: str, link: str, categories: list[str], preview_text: str, location=None):
    client = auth.OAuthAppClient(client_id, client_secret, app_id, app_token)
    preview_text = preview_text if preview_text != '' else content
    embed_id = client.Embed.create({"url": link})['embed_id']
    item_id = client.Item.create(app_id, attributes={"fields": {"titel": title, "datum-der-veroffentlichung": {
        "start_date": date.strftime("%Y-%m-%d"), "start_time": date.strftime("%H:%M")}, "inhalt": content,
                                                                "link-zum-artikel": embed_id,
                                                                "standort-optional": location,
                                                                "vorschau": preview_text}}, silent=True)['item_id']
    client.Tag.create("item", item_id, attributes=categories)


def get_last_date():
    client = auth.OAuthAppClient(client_id, client_secret, app_id, app_token)
    items = client.Item.filter(app_id,
                               attributes={"limit": 1, "sort_by": "datum-der-veroffentlichung", "sort_desc": True})
    try:
        return datetime.strptime(items['items'][0]['fields'][1]['values'][0]['start'], '%Y-%m-%d %H:%M:%S')
    except IndexError:
        return datetime.today() - timedelta(days=settings.delete_after)


def updated_status(message):
    client = auth.OAuthClient(client_id, client_secret, PODIO_EMAIL, PODIO_PASSWORD)
    client.Status.create(space_id, attributes={"value": message,
                                              "embed_url": "https://podio.com/api-test-o13qqzccw0/monitoring/apps/monitoring"})
    print(message)


def delete_outdated_articles():
    client = auth.OAuthAppClient(client_id, client_secret, app_id, app_token)
    items = client.Item.filter(app_id, attributes={"limit": 500, "filters":
        {"datum-der-veroffentlichung":
             {"from": datetime(2023, 1, 1).strftime("%Y-%m-%d"),
              "to": (datetime.today() - timedelta(days=settings.delete_after)).strftime("%Y-%m-%d")}}})

    # Temporary implementation to delete all items as bulk_delete isn't working for now
    for item in items['items']:
        client.Item.delete(item['item_id'])

    return items['filtered']


def get_config():
    client = auth.OAuthAppClient(client_id, client_secret, app_id, app_token)
    description = client.Application.find(app_id)['config']['description']
    refresh = re.search(r"Aktualisierungsintervall \(Stunden\): (\d+)", description)
    post_status = re.search(r"Status bei Aktualisierung schreiben: (Ja|Nein)", description)
    delete_after = re.search(r"Artikel löschen nach Tagen: (\d+)", description)
    return int(refresh.group(1)), int(delete_after.group(1)), post_status.group(1) == "Ja"


if __name__ == "__main__":
    print(get_config())
