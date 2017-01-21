from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '{{help}}'

    def handle(self, **options):
        self.stdout.write('{{name}} called')
