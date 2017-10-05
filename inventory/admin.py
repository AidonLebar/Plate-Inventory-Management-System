from django.contrib import admin
from .models import InventoryItem, Order, OrderItem


class InventoryItemAdmin(admin.ModelAdmin):
    fields = ['item_name', 'total_stock',]
    list_display = ('item_name', 'total_stock', 'current_stock')
    ordering = ['item_name']

    def current_stock(self, obj):
        return obj.currentStock()

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
    (None,          {'fields' : ['borrower_name','order_created', 'order_last_modified']}),
    ('Information', {'fields' : ['start_time', 'end_time']},),
    ]
    readonly_fields = ('order_created', 'order_last_modified', 'active')
    inlines = [OrderItemInline]
    list_display = ['borrower_name', 'start_time', 'end_time', 'active']
    ordering = ['-order_created']
    list_filter =['order_created']

    def active(self, obj):
        return obj.activeOrder()


admin.site.register(Order, OrderAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
