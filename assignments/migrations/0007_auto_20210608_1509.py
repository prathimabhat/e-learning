# Generated by Django 3.0.7 on 2021-06-08 09:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0006_auto_20210608_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='post_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
