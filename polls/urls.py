from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


#app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registration/', views.registration, name='registration'),

    path('coggle/', views.coggle_auth, name='coggle_auth'),

    path('<int:pk>/', views.HomeworksView.as_view(), name='homeworks'),
    path('<int:task_id>/<int:pk>', views.TasksView.as_view(), name='tasks'),
    path('<int:task_id>/add', views.homework_add, name='homework_add'),
    path('<int:task_id>/add/confirm', views.homework_add_confirm, name='homework_add_confirm'),

    path('<int:pk>/delete', views.HomeworkDelete.as_view(), name='homework_delete'),
    path('<int:task_id>/delete/<int:homework_id>/', views.homework_delete_page, name='homework_delete_page'),
    path('<int:task_id>/delete/<int:homework_id>/confirm', views.homework_delete_confirm, name='homework_delete_confirm'),

    path('add/', views.AddView.as_view(), name='add'),
    path('add/confirm', views.add_confirm, name='add_confirm'),

    path('change/', views.change, name='change'),
    path('change/<int:task_id>/', views.change_task, name='change_task'),
    path('change/<int:task_id>/confirm', views.change_task_confirm, name='change_task_confirm'),

    path('delete/', views.delete, name='delete'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('delete/<int:task_id>/confirm', views.delete_task_confirm, name='delete_task_confirm'),
]