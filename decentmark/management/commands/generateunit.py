from django.core.management.base import BaseCommand, CommandError
from decentmark.models import Unit

class Command(BaseCommand):
    help = 'Generate/regenerate unit with random content'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
