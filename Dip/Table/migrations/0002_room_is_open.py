# Generated by Django 5.1.5 on 2025-01-17 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Table', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_open',
            field=models.BooleanField(default=True),
        ),
    ]