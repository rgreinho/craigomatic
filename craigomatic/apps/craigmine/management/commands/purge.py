from django.core.management.base import BaseCommand

from craigslist.craigmine.indexing import delete_items


class Command(BaseCommand):
    help = "Purges the database."

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('days', type=int)

        # Named (optional) arguments
        parser.add_argument('--all',
                            action='store_true',
                            dest='all',
                            default=False,
                            help='Delete all items in the database.')

    def handle(self, *args, **options):
        if options['all']:
            days_old = 0
        elif options.get('days'):
            days_old = options.get('days')

        if not days_old:
            self.stdout.write('Nothing was purged.')
            return

        item_count = delete_items(days_old)
        self.stdout.write('{} items were deleted.'.format(item_count))
