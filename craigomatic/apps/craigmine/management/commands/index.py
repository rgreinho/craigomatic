from django.core.management.base import BaseCommand

from craigmine.indexing import run_all_searches


class Command(BaseCommand):
    help = "Indexes new search results."

    def handle(self, *args, **options):
        for content in run_all_searches():
            tag, found, count, last_update = content
            self.stdout.write("{} items found for '{}'.".format(found, tag))
            self.stdout.write("{} items created in '{}' (since {}).".format(count, tag, last_update))
