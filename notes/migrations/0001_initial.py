# Generated by Django 3.0.7 on 2021-05-27 14:56

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0016_auto_20210527_1824'),
        ('student_management', '0004_auto_20210516_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='notes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('file', models.FileField(default='', upload_to='')),
                ('note_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='accounts.Students')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='student_management.Subjects')),
            ],
            options={
                'verbose_name_plural': 'Notes',
            },
        ),
    ]
