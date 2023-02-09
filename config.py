import json


class Settings:
    def __init__(self):
        self.refresh_interval = 0
        self.delete_after = 0
        self.post_status_message = False
        self.read()

    def read(self):
        with open('config.json', 'r') as f:
            settings = json.loads(f.read())
            self.refresh_interval = int(settings['REFRESH_INTERVAL'])
            self.delete_after = int(settings['DELETE_AFTER'])
            self.post_status_message = int(settings['POST_STATUS_MESSAGE'])

    def write(self, refresh, delete, status):
        self.refresh_interval = refresh
        self.delete_after = delete
        self.post_status_message = status

        with open('config.json', 'w') as f:
            f.write(json.dumps({'REFRESH_INTERVAL': refresh,
                                'DELETE_AFTER': delete,
                                'POST_STATUS_MESSAGE': status}))
