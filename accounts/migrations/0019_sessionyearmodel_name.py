# Generated by Django 3.0.7 on 2021-06-07 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20210604_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionyearmodel',
            name='name',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
