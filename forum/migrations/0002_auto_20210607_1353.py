# Generated by Django 3.0.7 on 2021-06-07 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20210604_1843'),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='accounts.Staffs'),
        ),
        migrations.AddField(
            model_name='answers',
            name='teachers_forum',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='questions',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='accounts.Staffs'),
        ),
        migrations.AddField(
            model_name='questions',
            name='teachers_forum',
            field=models.BooleanField(default=False),
        ),
    ]