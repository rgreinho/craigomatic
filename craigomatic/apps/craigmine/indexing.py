from datetime import datetime
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from craigmine.craigslist import Craigslist
from craigmine.craigslist import querystring_to_dict
from craigmine.models import Item
from craigmine.models import Search


def get_all_search_ids():
    """
    Retrieves all the search IDs.

    :returns: all the search IDs.
    """
    # Retrieve all searches.
    search_ids = Search.objects.values('id')
    if not search_ids:
        return []
    return [d['id'] for d in search_ids]


def run_all_searches():
    """
    Run the indexing process for all the searches.

    :returns: A list of tuples containing the indexing results.
    """
    # Prepare variables.
    results = []

    # Retrieve all the available search ids.
    search_ids = get_all_search_ids()

    # Index each of them.
    for search_id in search_ids:
        indexed_summary = index_search_content(search_id)
        results.append(indexed_summary)

    # Return the results.
    return results


def index_search_content(search_id):
    """
    Returns a tuple containing information about the execution of the date indexed.

    This function ignores the entries that already exist in the databse.

    The returned tuple contains 4 values:
    * the tag describing the query
    * the number of found items
    * the number of indexed items
    * the date of the previous search update

    :param int search_id: ID of the search to index
    :returns: a tuple containing information about the execution of the date indexed.
    """

    # Load the search object.
    search = Search.objects.get(pk=search_id)

    # Load que the parameters.
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

    return (search.tag, len(requested_items), count, search.last_update)


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
