# Generated by Django 5.1.3 on 2024-11-29 06:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='date',
            new_name='start_date',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='duration',
        ),
        migrations.AddField(
            model_name='contract',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2024, 11, 30, 11, 12, 33, 186287), help_text='contract completion date'),
        ),
    ]
