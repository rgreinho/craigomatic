from django.core.exceptions import ObjectDoesNotExist

from django.core.management.base import BaseCommand

from craigmine.craigslist import Craigslist
from craigmine.models import Item
from craigmine.models import Search


class Command(BaseCommand):
    help = "Indexes new search results."

    def handle(self, *args, **options):
        tag, found, count, last_update = index_content()
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
    # Retrieve all searches.
    searches = Search.objects.all()

    for search in searches:
        queries = search.query
        custom_search_args = search.custom_search_args
        params = {"hasPic": search.has_pic,
                  "minAsk": search.min_ask,
                  "maxAsk": search.max_ask,
                  "s": 0,
                  "srchType": "T",
                  "sort": "date"}
        cl = Craigslist(search.server, search.category, params=params)

        # Prepare the query parameters.
        # for query in queries.split("|"):
        for custom_search_arg in custom_search_args.split('&'):

            # Try to split the query parameter to check whether it is a key/value pair.
            keyvalue = custom_search_arg.split('=', maxsplit=1)
            if len(keyvalue) == 2:
                cl.params[keyvalue[0]] = keyvalue[1]

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
                                    title=requested_item.get("title"))
                count += 1

        # Update the search.
        search.save()

        return search.tag, len(requested_items), count, search.last_update
