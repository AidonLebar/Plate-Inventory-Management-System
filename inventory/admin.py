from django.contrib import admin
from .models import InventoryItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem

class InventoryItemAdmin(admin.ModelAdmin):
    fields = ['item_name', 'total_stock']

class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
    (None,          {'fields' : ['borrower_name','order_created', 'order_last_modified']}),
    ('Information', {'fields' : ['start_time', 'end_time']},),
    ]
    readonly_fields = ('order_created', 'order_last_modified')
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
