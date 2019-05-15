from django.contrib import admin

from .models import UserData, Task, Homework


class TaskInline(admin.StackedInline):
    model = Task

class UserDataAdmin(admin.ModelAdmin):
    inlines = [TaskInline]

class HomeworkInline(admin.StackedInline):
    model = Homework

class TaskAdmin(admin.ModelAdmin):
    inlines = [HomeworkInline]

admin.site.register(UserData, UserDataAdmin)
admin.site.register(Task, TaskAdmin)

