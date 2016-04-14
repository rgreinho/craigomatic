from datetime import datetime
import time

from celery import group
from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

from craigmine.indexing import delete_items
from craigmine.indexing import get_all_search_ids
from craigmine.indexing import index_search_content

# Retrieve the Celery logger.
logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour='*/6')), ignore_result=True)
def prepare_indexing_tasks():
    logger.info('Collecting all the searches...')
    search_ids = get_all_search_ids()
    logger.info('{} search(es) collected.'.format(len(search_ids)))
    g = group(index_craigslist_content.s(i) for i in search_ids)
    res = g()
    logger.info("Task(s) dispatched!")


@shared_task
def index_craigslist_content(id):
    logger.info('Starting indexing search id: {}'.format(id))
    tag, found, count, last_update = index_search_content(id)
    logger.info("{} items found for '{}'.".format(found, tag))
    logger.info("{} items created in '{}' (since {}).".format(count, tag, last_update))
    logger.info('Indexing of search id: {} complete.'.format(id))


@periodic_task(run_every=(crontab(minute='*/1')), ignore_result=True)
def purge_content():
    item_max_age = 7
    logger.info('Deleting items older than {} day(s).'.format(item_max_age))
    item_count = delete_items(item_max_age)
    logger.info('{} item(s) were deleted.'.format(item_count))
