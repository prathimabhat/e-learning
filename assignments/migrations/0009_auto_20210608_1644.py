# Generated by Django 3.0.7 on 2021-06-08 11:14

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management', '0010_auto_20210607_1359'),
        ('assignments', '0008_remove_assignment_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='resources',
            name='link',
            field=models.URLField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='resources',
            name='text_resource',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='LectureLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(blank=True, max_length=300)),
                ('description', models.CharField(max_length=1000)),
                ('subject', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='lecturelinks', to='student_management.Subjects')),
            ],
        ),
    ]
