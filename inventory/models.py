import datetime

from django.db import models

class InventoryItem(models.Model):
    item_name = models.CharField(max_length = 100)
    total_stock = models.IntegerField()

    def __str__(self):
        return self.item_name

class Order(models.Model):
    borrower_name = models.CharField(max_length = 100)
    start_time = models.DateTimeField('Start Time')
    end_time = models.DateTimeField('End Time')
    order_created = models.DateTimeField('Created', auto_now_add = True)
    order_last_modified = models.DateTimeField('Last Modified', auto_now = False)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_borrowed = models.IntegerField()
    quantity_returned = models.IntegerField()

    def __str__(self):
        return '{} {}'.format(self.quantity_borrowed, self.item.item_name)
