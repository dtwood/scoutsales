from django.contrib import admin

from scoutsalesapp.models import Item, Transaction


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'sold_at']
    inlines = [ItemInline]


admin.site.register(Transaction, TransactionAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ['slug', 'seller_name', 'title', 'price', 'donation']


admin.site.register(Item, ItemAdmin)
