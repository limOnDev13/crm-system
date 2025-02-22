# Generated by Django 5.1.3 on 2024-11-30 12:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_alter_lead_phone'),
        ('contracts', '0003_alter_contract_end_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
                ('lead', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='clients.lead')),
            ],
        ),
    ]
