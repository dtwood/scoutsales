from django.contrib import admin

from scoutsalesapp.models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ['slug', 'seller_name', 'title', 'price', 'donation']
    pass


admin.site.register(Item, ItemAdmin)
