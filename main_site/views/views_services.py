import json
import requests
from requests.auth import HTTPBasicAuth

from main_site.models import UserData, coggle, miro
from main_site.views.views_tasks import task_add

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def coggle_auth_view(request):
    obj = coggle.Coggle(
        app_name=coggle.APP_NAME,
        client_id=coggle.CLIENT_ID,
        client_secret=coggle.CLIENT_SECRET,
        redirect_uri=coggle.REDIRECT_URI
    )
    obj.authorization()
    return redirect(task_add)


@login_required(login_url='/accounts/login/')
def coggle_get_code_view(request):
    try:
        code = request.GET['code']
    except Exception as e:
        print(e)
        context = {
            'title': "Ошибка токена",
            'text': "Ключ авторизации не был получен"
        }
        return render(request, 'main_site/actions/error.html', context)
    else:
        params = {
            'code': code,
            'grant_type': "authorization_code",
            'redirect_uri': coggle.REDIRECT_URI
        }
        response = requests.post(
            coggle.URL_BASE + "token",
            auth=HTTPBasicAuth(coggle.CLIENT_ID, coggle.CLIENT_SECRET),
            json=params
        )
        information_auth = json.loads(response.text)
        user_data = UserData.objects.get(user=request.user)
        user_data.coggle_key = information_auth['access_token']
        user_data.save()
        context = {
            'title': "Получение токена",
            'text': "Ключ авторизации был успешно получен"
        }
        return render(request, 'main_site/actions/done.html', context)


@login_required(login_url='/accounts/login/')
def miro_auth_view(request):
    obj = miro.Miro(
        app_name=miro.APP_NAME,
        client_id=miro.CLIENT_ID,
        client_secret=miro.CLIENT_SECRET,
        redirect_uri=miro.REDIRECT_URI
    )
    obj.authorization()
    return redirect(task_add)


@login_required(login_url='/accounts/login/')
def miro_get_code_view(request):
    try:
        code = request.GET['code']
    except Exception as e:
        print(e)
        context = {
            'title': "Ошибка токена",
            'text': "Ключ авторизации не был получен"
        }
        return render(request, 'main_site/actions/error.html', context)
    else:
        params = {
            'code': code,
            'grant_type': "authorization_code",
            'redirect_uri': miro.REDIRECT_URI
        }
        response = requests.post(
            miro.URL_BASE + "token",
            auth=HTTPBasicAuth(miro.CLIENT_ID, miro.CLIENT_SECRET),
            json=params
        )
        information_auth = json.loads(response.text)
        user_data = UserData.objects.get(user=request.user)
        user_data.miro_key = information_auth['access_token']
        user_data.save()
        context = {
            'title': "Получение токена",
            'text': "Ключ авторизации был успешно получен"
        }
        return render(request, 'main_site/actions/done.html', context)
