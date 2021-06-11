# Generated by Django 3.0.7 on 2021-06-11 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0018_quiz_enable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizanswers',
            name='question',
        ),
        migrations.AddField(
            model_name='quizanswers',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_answers', to='assignments.QuizQuestions'),
        ),
    ]
