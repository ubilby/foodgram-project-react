# Generated by Django 3.2.3 on 2023-10-28 16:47

import backend.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('cooking_time', models.PositiveSmallIntegerField(validators=[backend.validators.validate_positive])),
                ('text', models.TextField()),
                ('image', models.ImageField(default=None, null=True, upload_to='recipes/images/')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.CreateModel(
            name='RecipesIngredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[backend.validators.validate_positive])),
                ('ingredients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_used', to='ingredients.ingredients')),
                ('recipes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_used', to='recipes.recipes')),
            ],
        ),
    ]
