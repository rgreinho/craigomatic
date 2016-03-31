from django.core.exceptions import ObjectDoesNotExist

from django.core.management.base import BaseCommand

from craigmine.craigslist import Craigslist
from craigmine.craigslist import querystring_to_dict
from craigmine.models import Item
from craigmine.models import Search


class Command(BaseCommand):
    help = "Indexes new search results."

    def handle(self, *args, **options):
        for content in index_content():
            tag, found, count, last_update = content
            self.stdout.write("{} items found for '{}'.".format(found, tag))
            self.stdout.write("{} items created in '{}' (since {}).".format(count, tag, last_update))


def index_content():
    """
    Returns a tuple containing information about the execution of the date indexed.

    This function ignores the entries that already exist in the databse.

    The returned tuple contains 4 values:
    * the tag describing the query
    * the number of found items
    * the number of indexed items
    * the date of the previous search update

    :returns: a tuple containing information about the execution of the date indexed.
    """
    # Prepare results variable.
    results = []

    # Retrieve all searches.
    searches = Search.objects.all()
    if not searches:
        return results

    for search in searches:
        queries = search.query
        custom_search_args = search.custom_search_args
        params = {"hasPic": '1' if search.has_pic else '0',
                  "min_price": search.min_ask,
                  "max_price": search.max_ask,
                  "s": 0,
                  "sort": "date"}
        cl = Craigslist(search.server, search.category, params=params)

        # Prepare the query parameters.
        cl.params.update(querystring_to_dict(custom_search_args))

        # Retrieve and parse the items.
        requested_items = cl.query_n_parse()

        # Store them in the DB.
        count = 0
        for requested_item in requested_items.values():
            try:
                Item.objects.get(id=requested_item.get("clid"))
            except ObjectDoesNotExist:
                Item.objects.create(search=search,
                                    id=requested_item.get("clid"),
                                    link=requested_item.get("full_link"),
                                    post_date=requested_item.get("post_date"),
                                    pnr=requested_item.get("pnr"),
                                    price=requested_item.get("price"),
                                    title=requested_item.get("title", '?') or '?')
                count += 1

        # Update the search.
        search.save()

        results.append((search.tag, len(requested_items), count, search.last_update))

    return results
