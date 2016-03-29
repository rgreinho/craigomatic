from django.core.management.base import BaseCommand
from tabulate import tabulate

from craigmine.models import Item


class Command(BaseCommand):
    help = "Lists the result items."

    def handle(self, *args, **options):
        table = [[item.published_date, item.price, item.title, item.pnr]
                 for item in Item.objects.all().order_by("-post_date")]
        self.stdout.write(tabulate(table))
