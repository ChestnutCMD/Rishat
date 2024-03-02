from django.contrib import admin

from app.models import Item, Order, Discount, Tax


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('items',)
    readonly_fields = ('id', )


admin.site.register(Order, OrderAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'currency')
    search_fields = ('name', 'price')
    readonly_fields = ('id',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Discount)
admin.site.register(Tax)
