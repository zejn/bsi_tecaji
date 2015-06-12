from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Posodobi tecaje BSI'

    def add_arguments(self, parser):
        parser.add_argument('--full', dest='full', action='store_true', default=False)

    def handle(self, *args, **options):
        from bsi_tecaji.models import fetch, parse, load

        xmldata = fetch(full=options['full'])
        records = parse(xmldata, full=options['full'])
        load(records)


