from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),

    path('coggle/', views.coggle_get_code_view, name='coggle_get_code'),
    path('coggle/auth', views.coggle_auth_view, name='coggle_auth'),
    path('miro/', views.miro_get_code_view, name='miro_get_code'),
    path('miro/auth', views.miro_auth_view, name='miro_auth'),

    path('<int:task_id>/info', views.info_task_view, name='info_task'),

    path('<int:task_id>/', views.homeworks, name='homeworks'),
    path('<int:task_id>/<int:homework_id>', views.homework, name='homework'),
    path('<int:task_id>/add', views.homework_add, name='homework_add'),
    path('<int:task_id>/add/confirm', views.homework_add_confirm, name='homework_add_confirm'),

    path('<int:task_id>/delete', views.homework_delete, name='homework_delete'),
    path('<int:task_id>/delete/<int:homework_id>/', views.homework_delete_page, name='homework_delete_page'),
    path('<int:task_id>/delete/<int:homework_id>/confirm', views.homework_delete_confirm, name='homework_delete_confirm'),

    path('add/', views.task_add, name='add'),
    path('add/confirm', views.task_add_confirm, name='add_confirm'),

    path('change/', views.change, name='change'),
    path('change/<int:task_id>/', views.change_task, name='change_task'),
    path('change/<int:task_id>/confirm', views.change_task_confirm, name='change_task_confirm'),

    path('delete/', views.delete, name='delete'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('delete/<int:task_id>/confirm', views.delete_task_confirm, name='delete_task_confirm'),
]
