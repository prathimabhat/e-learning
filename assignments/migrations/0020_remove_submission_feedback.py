# Generated by Django 3.0.7 on 2021-06-11 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0019_auto_20210611_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='feedback',
        ),
    ]
