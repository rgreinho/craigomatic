from django.db import models
from django.utils.html import format_html


# Create your models here.
class Search(models.Model):
    """
    http://austin.craigslist.org/search/bia?sort=date&hasPic=1&minAsk=10&maxAsk=250&query=fixed
    """
    server = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    has_pic = models.BooleanField(default=True)
    min_ask = models.PositiveIntegerField(default=0)
    max_ask = models.PositiveIntegerField(default=1000)
    query = models.CharField(max_length=300, default='')
    tag = models.CharField(max_length=20)
    custom_search_args = models.CharField(max_length=300, default='')
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag


class Item(models.Model):
    search = models.ForeignKey(Search)
    id = models.CharField(primary_key=True, max_length=200)
    link = models.URLField()
    post_date = models.DateTimeField()
    pnr = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    retrieved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def external_link(self):
        return format_html('<a href="{0}">{0}</a>', self.link)

    external_link.allow_tags = True
