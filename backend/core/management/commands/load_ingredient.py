import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


ROUTE = 'core/data/ingredients.csv'


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из csv файла'

    def handle(self, *args, **options):
        with open(ROUTE, 'r', encoding='UTF-8') as csv_file:
            csvreader = csv.reader(csv_file)
            for row in csvreader:
                Ingredient.objects.bulk_create(
                    [Ingredient(
                        name=row[0],
                        measurement_unit=row[1]
                    )]
                )
        print('Загрузка завершена.')
