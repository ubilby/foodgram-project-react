# Generated by Django 3.2.3 on 2023-10-23 17:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator('^#[0-9A-Fa-f]{6}$', message='Неверный формат цвета.')])),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]
