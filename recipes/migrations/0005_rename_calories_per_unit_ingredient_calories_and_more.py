# Generated by Django 5.1.2 on 2024-10-21 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_remove_recipe_ingredients_recipeingredient_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='calories_per_unit',
            new_name='calories',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='carbs_per_unit',
            new_name='carbs',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='fat_per_unit',
            new_name='fat',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='protein_per_unit',
            new_name='protein',
        ),
        migrations.RemoveField(
            model_name='recipeingredient',
            name='unit',
        ),
        migrations.AddField(
            model_name='recipe',
            name='total_calories',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
