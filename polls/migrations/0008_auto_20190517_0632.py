# Generated by Django 2.2.1 on 2019-05-17 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20190517_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='plagiarism',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='homework',
            name='similarity',
            field=models.IntegerField(default=0),
        ),
    ]