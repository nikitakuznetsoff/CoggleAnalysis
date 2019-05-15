import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Task(models.Model):
    title = models.CharField(max_length=200)
    about = models.CharField(max_length=400)
    userData = models.ForeignKey(UserData, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Homework(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    similarity = models.FloatField(default=-1)
    plagiarism = models.FloatField(default=-1)


    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


