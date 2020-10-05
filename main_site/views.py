import json
import requests

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

import django.contrib.auth.forms as f

from openpyxl import load_workbook
from requests.auth import HTTPBasicAuth

from modules import checks, coggle, readers, analysis, text_search
from .models import UserData, Task, Homework


# def registration(request):
#     form = UserCreationForm(request.POST)
#     if form.is_valid():
#         form.save()
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password1')
#         user = authenticate(username=username, password=password)
#         login(request, user)
#         return redirect('index')
#     # else:
#     #     form = UserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='/accounts/login/')
def index(request):
    # coggle.coggle_user.authorization()
    try:
        user_data = UserData.objects.get(user=request.user)
    except UserData.DoesNotExist:
        user_data = ''
    context = {'userData': user_data}
    return render(request, 'main_site/index.html', context)


@login_required(login_url='/accounts/login/')
def homeworks(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        task = ''
    context = {'task': task}
    return render(request, 'main_site/actions/homeworks/list.html', context)


@login_required(login_url='/accounts/login/')
def homework(request, task_id, homework_id):
    try:
        hw = Homework.objects.get(pk=homework_id)
    except Homework.DoesNotExist:
        hw = ''
    context = {
        'task_id': task_id,
        'homework': hw
    }
    return render(request, 'main_site/actions/homeworks/homework.html', context)


class TasksView(LoginRequiredMixin, generic.DetailView):
    model = Homework
    template_name = 'main_site/actions/homeworks/homework.html'


@login_required(login_url='/accounts/login/')
def homework_add(request, task_id):
    context = {'task_id': task_id}
    return render(request, 'main_site/actions/homeworks/create.html', context)


@login_required(login_url='/accounts/login/')
def homework_add_confirm(request, task_id):
    try:
        name = request.POST['name']
        link = request.POST['link']
        link = readers.link_to_id(link)
    except Exception:
        context = {
            'title': "Добавление работы",
            'text': "Произошла ошибка при добавлении работы"
        }
        return render(request, 'main_site/actions/error.html', context)
    else:
        user_data = UserData.objects.get(user=request.user)
        task = user_data.task_set.get(pk=task_id)
        task.homework_set.create(name=name, link=link)

        context = {
            'title': "Добавление работы",
            'text': "Работа успешно добалена"
        }
        return render(request, 'main_site/actions/done.html', context)


@login_required(login_url='/accounts/login/')
def homework_delete(request, task_id):
    task = Task.objects.get(pk=task_id)
    context = {
        'task': task,
    }
    return render(request, 'main_site/actions/homeworks/delete.html', context)

# class HomeworkDelete(LoginRequiredMixin, generic.DetailView):
#     model = Task
#     template_name = 'main_site/actions/homeworks/delete.html'


@login_required(login_url='/accounts/login/')
def homework_delete_page(request, task_id, homework_id):
    task = Task.objects.get(pk=task_id)
    homework = task.homework_set.get(pk=homework_id)
    context = {
        'task_id': task_id,
        'homework': homework
    }
    return render(request, 'main_site/actions/homeworks/delete_confirm.html', context)


@login_required(login_url='/accounts/login/')
def homework_delete_confirm(request, task_id, homework_id):
    task = Task.objects.get(pk=task_id)
    homework = task.homework_set.get(pk=homework_id)
    try:
        homework.delete()
    except Exception:
        context = {
            'title': "Удаление работы",
            'text': "Произошла ошибка, работы не удалена"
        }
        return render(request, 'main_site/actions/error.html', context)
    else:
        context = {
            'title': "Удаление работы",
            'text': "Работа успешно удалена"
        }
        return render(request, 'main_site/actions/done.html', context)

########################


class AddView(LoginRequiredMixin, generic.ListView):
    model = UserData
    template_name = 'main_site/actions/add.html'


@login_required(login_url='/accounts/login/')
def add_confirm(request):
    try:
        title_new = request.POST['title']
        about_new = request.POST['about']
        file = request.FILES['file_table']
        table_name = request.POST['table']

        true_work = request.POST['true_work']
        true_work_link = readers.link_to_id(true_work)

        keys = request.POST['keys']
        names_column = request.POST['names']
        links_column = request.POST['links']
        start_row = request.POST['row']

    except Exception as e:
        print(e)
        context = {
            'title': "Создание задания",
            'text': "Произошла ошибка при создании задания"
        }
        return render(request, 'main_site/actions/error.html', context)
    else:
        try:
            # Проверка наличия токена для анализа
            if coggle.coggle_user.access_token == "":
                coggle.coggle_user.authorization()
                # return render(request, 'main_site/actions/add.html')
        except Exception:
            context = {
                'title': "Создание задания",
                'text': "Произошла ошибка при создании задания"
            }
            return render(request, 'main_site/actions/error.html', context)

        wb = load_workbook(filename=file, read_only=True)
        # Проверка наличия заданной таблицы в Excel файле
        if table_name != '':
            if not checks.check_correct_tablename(wb, table_name):
                context = {
                    'title': "Создание задания",
                    'text': "Произошла ошибка при создании задания"
                }
                return render(request, 'main_site/actions/error.html', context)

        # Проверка формата заданных ячеек
        if not checks.check_correct_column_name(names_column) \
                or not checks.check_correct_column_name(links_column) \
                or not checks.check_correct_row_name(start_row):
            context = {
                'title': "Создание задания",
                'text': "Ошибка в формате столбцов / ячеек"
            }
            return render(request, 'main_site/actions/error.html', context)

        # try:
        #     # Проверка наличия токена для анализа
        #     if coggle.coggle_user.access_token == "":
        #         coggle.coggle_user.authorization()
        #         return render(request, 'main_site/actions/add.html')
        # except Exception:
        #     context = {
        #         'title': "Создание задания",
        #         'text': "Произошла ошибка при создании задания"
        #     }
        #     return render(request, 'main_site/actions/error.html', context)

        # Создание объекта домашнего задания для текущего пользователя
        curr_data = UserData.objects.get(user=request.user)
        curr_task = curr_data.task_set.create(title=title_new, about=about_new)
        print("[CREATING TASK] TITLE: " + title_new + "; ABOUT: " + about_new)

        # Создание массива ключевых значений
        arr_keys = keys.split(",")

        # Загрузка нужной таблицы
        wb = load_workbook(file)
        if table_name != '':
            sheet = wb[table_name]
        else:
            sheet = wb[wb.sheetnames[0]]

        print("[SHEET] " + str(sheet))
        # Чтение информации из таблицы
        arr = readers.read_mindmap_ids(sheet, names_column, links_column, start_row)
        print("IDs: " + str(arr))
        # Получение массива коэффициентов структурного сходства
        arr_with_coef = analysis.mindmap_analysis(arr[1], true_work_link)

        # Массив текстов каждой интеллект карты
        # arr_text = analysis.take_text(arr[1])

        sim_arr = []
        # # Массив с вычисленными сходствами текстовых составляющих
        # if len(arr_keys) > 0:
        #     sim_arr = text_search.initialization(arr_keys, arr_text)
        # else:
        #     sim_arr = [0] * len(arr_keys)

        # Создание работ
        for i in range(0, len(arr[0])):
            # Проверка на считывание лишней информации
            if arr[0][i] is None:
                break
            if true_work_link == "":
                coef = round(arr_with_coef[1][i] * 100)
            else:
                coef = round(arr_with_coef[i] * 100)

            if len(sim_arr) > 0:
                sim = round(sim_arr[i] * 100)
            else:
                sim = -1
            print("[ADDING HW] NAME: " + arr[0][i])
            curr_task.homework_set.create(name=arr[0][i], link=arr[1][i],
                                          similarity=coef, plagiarism=sim)

        context = {
            'title': "Создание задания",
            'text': "Задание успешно добавлено"
        }
        return render(request, 'main_site/actions/done.html', context)


########################

@login_required(login_url='/accounts/login/')
def change(request):
    try:
        user_data = UserData.objects.get(user=request.user)
    except UserData.DoesNotExist:
        user_data = ''
    context = {'userData': user_data}
    return render(request, 'main_site/actions/change.html', context)


@login_required(login_url='/accounts/login/')
def change_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    context = {'task': task,
               'task_id' : task_id}
    return render(request, 'main_site/actions/change_confirm.html', context)


@login_required(login_url='/accounts/login/')
def change_task_confirm(request, task_id):
    task = Task.objects.get(pk=task_id)
    try:
        title_new = request.POST['title']
        about_new = request.POST['about']
    except:
        context = {
            'title': "Изменение описания",
            'text': "Произошла ошибка, изменения не сохранены"
        }
        return render(request, 'main_site/actions/error.html', context)
    else:
        task.title = title_new
        task.about = about_new
        task.save()
        context = {
            'title': "Изменение описания",
            'text': "Изменения успешно сохранены"
        }
        return render(request, 'main_site/actions/done.html', context)


########################

@login_required(login_url='/accounts/login/')
def delete(request):
    try:
        user_data = UserData.objects.get(user=request.user)
    except UserData.DoesNotExist:
        user_data = ''
    context = {'userData': user_data}
    return render(request, 'main_site/actions/delete.html', context)


@login_required(login_url='/accounts/login/')
def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    context = {
        'task': task,
        'task_id': task_id
    }
    return render(request, 'main_site/actions/delete_confirm.html', context)


@login_required(login_url='/accounts/login/')
def delete_task_confirm(request, task_id):
    task = Task.objects.get(pk=task_id)
    try:
        task.delete()
    except:
        context = {
            'title': "Удаление задание",
            'text': "Произошла ошибка при удалении задания"
        }
        return render(request, 'main_site/actions/error.html', context)
    else:
        context = {
            'title': "Удаление задания",
            'text': "Задание успешно удалено"
        }
        return render(request, 'main_site/actions/done.html', context)


########################


@login_required(login_url='/accounts/login/')
def coggle_auth(request):
    try:
        code = request.GET['code']
    except Exception:
        context = {
            'title': "Ошибка токена",
            'text': "Ключ авторизации не был получен"
        }
        return render(request, 'main_site/actions/error.html', context)
    else:
        params = {"code": code, "grant_type": "authorization_code", "redirect_uri": coggle.redirect_uri}
        resp1 = requests.post(coggle.coggle_user.url_base + "token", auth=HTTPBasicAuth(coggle.client_id, coggle.client_secret), json=params)
        information_auth = json.loads(resp1.text)
        coggle.coggle_user.access_token = information_auth["access_token"]

        context = {
            'title': "Получение токена",
            'text': "Ключ авторизации был успешно получен"
        }
    return render(request, 'main_site/actions/done.html', context)
