from django.core.management.base import BaseCommand

import json

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка данных в базу'
    command_name = 'load_data'

    def handle(self, *args, **options):

        if not Ingredient.objects.exists():
            with open(
                'recipes/data/ingredients.json', 'r', encoding='utf-8'
            ) as data:
                loaded_data = json.load(data)
                Ingredient.objects.bulk_create(
                    objs=[
                        Ingredient(**ingredient_data)
                        for ingredient_data in loaded_data
                    ]
                )
                print('Ингредиенты загружены')
        else:
            print('Данные уже есть в БД')
