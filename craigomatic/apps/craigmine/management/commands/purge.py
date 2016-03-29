from datetime import datetime
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from craigmine.models import Item


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


def delete_items(days_old):
    """
    Deletes the items older than a certain amount of days.

    If days_old is set to 0, *ALL* the objects will be deleted.

    :param int days_old: the number of days defining the threshold
    :return: the number of deleted items.
    """
    days_ago = datetime.today() - timedelta(days=days_old)
    items = Item.objects.filter(post_date__lt=timezone.make_aware(days_ago))
    item_count = len(items)
    items.delete()

    return item_count
