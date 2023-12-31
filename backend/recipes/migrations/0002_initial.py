# Generated by Django 3.2.3 on 2023-10-30 12:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredients', '0001_initial'),
        ('recipes', '0001_initial'),
        ('tags', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='recipes',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_used', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.RecipesIngredients', to='ingredients.Ingredients'),
        ),
        migrations.AddField(
            model_name='recipes',
            name='tags',
            field=models.ManyToManyField(to='tags.Tag'),
        ),
    ]
