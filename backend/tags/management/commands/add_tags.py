from django.core.management.base import BaseCommand

from tags.models import Tag


class Command(BaseCommand):
    help = 'Create some tags'

    def handle(self, *args, **options):
        if not Tag.objects.all().exists():
            Tag.objects.create(name='dinner', color='#ff0000', slug='dinner')
            Tag.objects.create(
                name='breakfast', color='#ff0000', slug='breakfast')
            Tag.objects.create(name='lunch', color='#ff0000', slug='lunch')
            self.stdout.write(self.style.SUCCESS(
                'Tags create successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS(
                'Tags alredy create successfully.'))
