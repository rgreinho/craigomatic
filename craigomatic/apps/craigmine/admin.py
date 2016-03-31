from django.contrib import admin

# Register your models here.
from .models import Search
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ("search", "post_date", "price", "title", "pnr", "external_link", "retrieved")
    ordering = ("search", "-retrieved")


admin.site.register(Search)
admin.site.register(Item, ItemAdmin)
