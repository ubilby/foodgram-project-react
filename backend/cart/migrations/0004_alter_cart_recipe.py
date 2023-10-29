# Generated by Django 3.2.3 on 2023-10-29 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_remove_recipes_subscriptions'),
        ('cart', '0003_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='recipes.recipes'),
        ),
    ]
