# Generated by Django 3.0.7 on 2021-05-17 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20210516_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='session_year_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student', to='accounts.SessionYearModel'),
        ),
    ]
