# Generated by Django 4.1.7 on 2023-06-05 16:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'избранный рецепт',
                'verbose_name_plural': 'избранные рецепты',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название рецепта')),
                ('cooking_time', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, 'минимальное время приготовления 1 минута')], verbose_name='Время приготовления')),
                ('text', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(blank=True, upload_to='img_recipe/', verbose_name='Загрузить фото')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='время добавления')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(verbose_name='количество')),
            ],
            options={
                'verbose_name': 'ингредиент в рецепте',
                'verbose_name_plural': 'ингредиенты в рецепте',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название тега')),
                ('color', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(code='invalid_hex', message='Invalid hex code', regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')], verbose_name='Цвет')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_carts', to='recipes.recipe', verbose_name='рецепт')),
            ],
            options={
                'verbose_name': 'рецепт в корзине',
                'verbose_name_plural': 'рецепты в корзине',
            },
        ),
    ]
