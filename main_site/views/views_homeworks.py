from main_site.models import UserData, Task, Homework

from modules import readers

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def homeworks(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        task = ''
    context = {
        'task_id': task_id,
        'task': task
    }
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


@login_required(login_url='/accounts/login/')
def homework_add(request, task_id):
    context = {
        'task_id': task_id
    }
    return render(request, 'main_site/actions/homeworks/create.html', context)


@login_required(login_url='/accounts/login/')
def homework_add_confirm(request, task_id):
    try:
        name = request.POST['name']
        link = request.POST['link']
        link = readers.link_to_id(link)
    except Exception as e:
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
        'task_id': task_id,
        'task': task,
    }
    return render(request, 'main_site/actions/homeworks/delete.html', context)


@login_required(login_url='/accounts/login/')
def homework_delete_page(request, task_id, homework_id):
    task = Task.objects.get(pk=task_id)
    homework = task.homework_set.get(pk=homework_id)
    context = {
        'task_id': task_id,
        'task': task,
        'homework': homework
    }
    return render(request, 'main_site/actions/homeworks/delete_confirm.html', context)


@login_required(login_url='/accounts/login/')
def homework_delete_confirm(request, task_id, homework_id):
    task = Task.objects.get(pk=task_id)
    homework = task.homework_set.get(pk=homework_id)
    try:
        homework.delete()
    except Exception as e:
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
