from django.contrib import admin

from scoutsalesapp.models import Item, Transaction


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'sold_at']
    inlines = [ItemInline]


admin.site.register(Transaction, TransactionAdmin)


@admin.action(description="Make scouts")
def make_published(modeladmin, request, queryset):
    queryset.update(seller_email="scouts@newnhamscouts.org.uk", donation=100, seller_name="Scout Group")


class ItemAdmin(admin.ModelAdmin):
    list_display = ['slug', 'seller_name', 'title', 'price', 'donation']
    actions = [make_published]


admin.site.register(Item, ItemAdmin)
