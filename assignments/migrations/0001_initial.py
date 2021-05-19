# Generated by Django 3.0.7 on 2021-05-08 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student_management', '0003_feedbackparent_notificationparent'),
        ('accounts', '0005_auto_20210502_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=1000)),
                ('file', models.FileField(default='', upload_to='')),
                ('post_time', models.CharField(max_length=100)),
                ('deadline', models.CharField(max_length=100)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment', to='student_management.Subjects')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_submitted', models.FileField(default='', upload_to='')),
                ('time_submitted', models.CharField(max_length=100)),
                ('feedback', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('assignment', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='submission', to='assignments.Assignment')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='submission', to='accounts.Students')),
            ],
        ),
    ]