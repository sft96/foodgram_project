# Generated by Django 4.1.7 on 2023-06-10 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_recipe_author_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommandHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('is_executed', models.BooleanField(default=False)),
            ],
        ),
    ]