# Generated by Django 3.1.1 on 2020-10-08 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='coggle_key',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='miro_key',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
    ]
