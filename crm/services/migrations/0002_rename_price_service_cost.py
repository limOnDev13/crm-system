# Generated by Django 5.1.3 on 2024-11-27 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='price',
            new_name='cost',
        ),
    ]
