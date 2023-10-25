from django.core.management.base import BaseCommand

import json

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Загрузка данных о тегах в базу'
    command_name = 'load_data'

    def handle(self, *args, **options):

        if not Tag.objects.exists():
            with open(
                'recipes/data/tags.json', 'r', encoding='utf-8'
            ) as data:
                loaded_data = json.load(data)
                Tag.objects.bulk_create(
                    objs=[
                        Tag(**tag_data)
                        for tag_data in loaded_data
                    ]
                )
                print('Теги загружены')
        else:
            print('Данные уже есть в БД')
