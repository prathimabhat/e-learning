# Generated by Django 3.0.7 on 2021-05-27 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_notes_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]