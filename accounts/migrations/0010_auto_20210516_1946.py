# Generated by Django 3.0.7 on 2021-05-16 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20210516_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffs',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='dob',
            field=models.DateField(null=True),
        ),
    ]