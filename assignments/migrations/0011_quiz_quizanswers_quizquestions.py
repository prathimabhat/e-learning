# Generated by Django 3.0.7 on 2021-06-10 10:50

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_sessionyearmodel_name'),
        ('student_management', '0010_auto_20210607_1359'),
        ('assignments', '0010_auto_20210609_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizQuestions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('question_type', models.CharField(max_length=50, null=True)),
                ('question_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('question_marks', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuizAnswers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('answer_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('answered_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_answers', to='assignments.QuizQuestions')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_answers', to='accounts.Students')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('quiz_name', models.CharField(blank=True, max_length=300, null=True)),
                ('quiz_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_marks', models.PositiveIntegerField(null=True)),
                ('min_marks', models.PositiveIntegerField(null=True)),
                ('time_for_quiz', models.TimeField()),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='accounts.Staffs')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='student_management.Subjects')),
            ],
        ),
    ]
