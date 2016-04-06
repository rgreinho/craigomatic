from datetime import datetime

from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

# Retrieve the Celery logger.
logger = get_task_logger(__name__)


# An example task.
# A periodic task that will run every minute.
@periodic_task(run_every=(crontab(minute='*/1')), name="scraper_example", ignore_result=False)
def scraper_example():
    logger.info("Start task")
    now = datetime.now()
    logger.info("Task finished!")
