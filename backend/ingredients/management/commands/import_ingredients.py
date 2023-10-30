from django.core.management.base import BaseCommand

from ingredients.models import Ingredients


class Command(BaseCommand):
    help = 'Import ingredients from a file'

    def handle(self, *args, **options):
        with open('ingredients.csv', 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line[0] == '"':
                name = line[1: -2]
                unit = line[-1]
            else:
                data = line.strip().split(',')
                name = data[0]
                unit = data[1]

            ingredient = Ingredients(name=name, measurement_unit=unit)

        self.stdout.write(self.style.SUCCESS(
            'Ingredients imported successfully.'))
