from django.db import models
from django.contrib.auth.models import User


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coggle_key = models.CharField(max_length=300, null=True, default=None)
    miro_key = models.CharField(max_length=300, null=True, default=None)

    def __str__(self):
        return self.user.username


class Task(models.Model):
    title = models.CharField(max_length=200, null=True)
    about = models.CharField(max_length=400, null=True)
    keys = models.CharField(max_length=1000, null=True)

    userData = models.ForeignKey(UserData, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Homework(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    link = models.CharField(max_length=100, null=True)
    service = models.CharField(max_length=30, null=True)

    # Metrics
    similarity_score = models.IntegerField(default=0)
    text_score = models.IntegerField(default=0)
    text_keys = models.CharField(max_length=10000, null=True)
    plagiarism = models.IntegerField(default=0)

    count_nodes = models.IntegerField(default=0)
    count_first_layer_branches = models.IntegerField(default=0)
    average_node_text = models.IntegerField(default=0)
    max_height = models.IntegerField(default=0)
    text_length = models.IntegerField(default=0)

    def __str__(self):
        return self.name
