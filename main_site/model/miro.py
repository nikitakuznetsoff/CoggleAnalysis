import requests
import webbrowser


# Класс для основных операций с API
class Miro:
    def __init__(self, app_name, client_id, client_secret, redirect_uri, access_token=""):
        self.app_name = app_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.url_base = "https://miro.com/"
        self.access_token = access_token

    # Авторизация
    def authorization(self):
        params = {
            'response_type': "code",
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri
        }
        resp_auth = requests.get(self.url_base + 'oauth/authorize/', params=params)
        webbrowser.open_new_tab(resp_auth.url)


APP_NAME = "cognitive-maps-parser"
CLIENT_ID = "3074457350265036612"
CLIENT_SECRET = "cL72NzOBDNUhOhqZqbVOOZmM9zfmeHye"
REDIRECT_URI = "http://127.0.0.1:8000:8000/miro"
URL_BASE = "https://miro.com/"