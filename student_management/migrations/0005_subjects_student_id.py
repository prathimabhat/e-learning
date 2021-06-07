# Generated by Django 3.0.8 on 2021-06-06 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20210604_1843'),
        ('student_management', '0004_auto_20210516_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjects',
            name='student_id',
            field=models.ManyToManyField(null=True, related_name='student', to='accounts.Students'),
        ),
    ]