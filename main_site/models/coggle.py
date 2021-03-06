import requests
import json
from urllib.parse import urlencode
from django.shortcuts import redirect

# Класс для основных операций с API
class Coggle:
    def __init__(self, app_name, client_id, client_secret, redirect_uri, access_token=""):
        self.app_name = app_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.url_base = "https://coggle.it/"
        self.access_token = access_token

    # Авторизация
    def authorization(self):
        params = {
            'response_type': "code",
            'scope': "read",
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri
        }
        return redirect(self.url_base + 'dialog/authorize?' + urlencode(params))

    # Получение информации о всей диаграмме
    def diagram(self, id_diagram):
        params = {"access_token": self.access_token}
        url_diagram = "api/1/diagrams/"
        diagram_info = requests.get(
            self.url_base + url_diagram + id_diagram,
            params=params
        )
        diagram = json.loads(diagram_info.text)
        return diagram

    # Получение информации о вершинах
    def nodes(self, id_diagram):
        params = {"access_token": self.access_token}
        url_diagram = "api/1/diagrams/"
        nodes_info = requests.get(
            url=self.url_base + url_diagram + id_diagram + "/nodes",
            params=params
        )
        nodes = json.loads(nodes_info.text)
        return nodes

    def __str__(self):
        return "Coggle"


APP_NAME = "CourseWork"
CLIENT_ID = "5a8ab7821c5b5b00010853f0"
CLIENT_SECRET = "8df4c6d49cfbf495ff57c21263269209c18596e35edb07abe53e311f918272ec"
REDIRECT_URI = "http://127.0.0.1:8000/coggle"
URL_BASE = "https://coggle.it/"