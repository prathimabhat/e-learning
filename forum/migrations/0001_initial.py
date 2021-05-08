# Generated by Django 3.0.7 on 2021-05-08 06:04

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0005_auto_20210502_1628'),
        ('student_management', '0003_feedbackparent_notificationparent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('question_title', models.CharField(blank=True, max_length=300, null=True)),
                ('question_detail', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('anonymous', models.BooleanField(default=False)),
                ('down_votes', models.ManyToManyField(related_name='questions_down_votes', to='accounts.Students')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='student_management.Subjects')),
                ('up_votes', models.ManyToManyField(related_name='questions_up_votes', to='accounts.Students')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='accounts.Students')),
            ],
            options={
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('answer', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('anonymous', models.BooleanField(default=False)),
                ('down_votes', models.ManyToManyField(related_name='answers_down_votes', to='accounts.Students')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='forum.Questions')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='student_management.Subjects')),
                ('up_votes', models.ManyToManyField(related_name='answers_up_votes', to='accounts.Students')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='accounts.Students')),
            ],
            options={
                'verbose_name_plural': 'Answers',
            },
        ),
    ]
