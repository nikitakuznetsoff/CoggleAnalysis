import requests
import json
from urllib.parse import urlencode
from django.shortcuts import redirect


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
        return redirect(self.url_base + 'oauth/authorize?' + urlencode(params))

    def nodes(self, id_diagram):
        params = {'access_token': self.access_token}
        url_diagram = 'https://api.miro.com/v1/boards/'

        nodes_info = requests.get(
            url=url_diagram + id_diagram + "/widgets/",
            params=params
        )
        nodes = json.loads(nodes_info.text)
        return nodes

    def __str__(self):
        return "Miro"


APP_NAME = "cognitive-maps-parser"
CLIENT_ID = "3074457350265036612"
CLIENT_SECRET = "cL72NzOBDNUhOhqZqbVOOZmM9zfmeHye"
REDIRECT_URI = "http://localhost:8000/miro"
URL_BASE = "https://miro.com/"
