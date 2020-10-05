import requests
import json
import webbrowser

from requests.auth import HTTPBasicAuth


# Класс для основных операций с API
class Coggle:
    def __init__(self, app_name, client_id, client_secret, redirect_uri):
        self.app_name = app_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.url_base = "https://coggle.it/"
        self.access_token = ""

    # Авторизация
    def authorization(self):
        params = {'response_type': "code", 'scope': "read", 'client_id': self.client_id, 'redirect_uri': self.redirect_uri}
        resp_auth = requests.get(self.url_base + 'dialog/authorize/', params=params)
        webbrowser.open_new_tab(resp_auth.url)


    def authorization_token(self):
        code = requests.get('code')
        params = {"code": code, "grant_type": "authorization_code", "redirect_uri": self.redirect_uri}
        resp1 = requests.post(self.url_base + "token", auth=HTTPBasicAuth(client_id, self.client_secret), json=params)
        information_auth = json.loads(resp1.text)
        self.access_token = information_auth["access_token"]

    # Получение информации о всей диаграмме
    def diagram(self, id_diagram):
        params = {"access_token": self.access_token}
        url_diagram = "api/1/diagrams/"
        information_diagram = requests.get(self.url_base + url_diagram + id_diagram, params=params)
        diagram = json.loads(information_diagram.text)
        return diagram

    # Получение информации о вершинах
    def nodes(self, id_diagram):
        params = {"access_token": self.access_token}
        url_diagram = "api/1/diagrams/"
        information_nodes = requests.get(self.url_base + url_diagram + id_diagram + "/nodes", params=params)
        nodes = json.loads(information_nodes.text)
        return nodes


app_name = "CourseWork"
client_id = "5a8ab7821c5b5b00010853f0"
client_secret = "8df4c6d49cfbf495ff57c21263269209c18596e35edb07abe53e311f918272ec"
redirect_uri = "http://127.0.0.1:8000/coggle"

coggle_user = Coggle(app_name, client_id, client_secret, redirect_uri)