# Generated by Django 3.2 on 2021-06-09 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_alter_customuser_first_name'),
        ('student_management', '0010_auto_20210607_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjects',
            name='session_year_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.sessionyearmodel'),
        ),
    ]