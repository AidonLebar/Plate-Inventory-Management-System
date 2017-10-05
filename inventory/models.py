import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.db import models

class InventoryItem(models.Model):
    item_name = models.CharField(max_length = 100)
    total_stock = models.PositiveIntegerField()

    def __str__(self):
        return self.item_name

    def currentStock(self): #calculates current stock as total - currently out
        stock = self.total_stock
        for  i in self.orderitem_set.all():
            if i.activeOrderItem():
                stock = stock - i.quantity_borrowed
        return stock

    def averageOrder(self):
        average = 0
        for i in self.orderitem_set.all():
            average = average + i.quantity_borrowed
        average = average/self.orderitem_set.count()

        return average

class Order(models.Model):
    borrower_name = models.CharField(max_length = 100)
    start_time = models.DateTimeField('Start Time')
    end_time = models.DateTimeField('End Time')
    order_created = models.DateTimeField('Created', auto_now_add = True)
    order_last_modified = models.DateTimeField('Last Modified', auto_now = True)

    def __str__(self):
        start_date = self.start_time.strftime('%Y-%m-%d')
        return '{} : {}'.format(self.borrower_name, start_date)

    def activeOrder(self):
        now = timezone.now()
        return (now >= self.start_time) and (now <= self.end_time)

    def clean(self):
        if self.start_time is None:
            raise ValidationError("Start time cannot be empty")

        if self.end_time is None:
            raise ValidationError("End time cannot be empty")

        if self.end_time < self.start_time:
            raise ValidationError("Start time must be before end time")

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_borrowed = models.PositiveIntegerField()
    quantity_returned = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.quantity_borrowed, self.item.item_name)

    def activeOrderItem(self):
        return self.order.activeOrder();

    def itemDelta(self):
        return self.quantity_borrowed - self.quantity_returned

    def clean(self):
        if self.quantity_returned > self.quantity_borrowed:
            raise ValidationError("Cannot return more than was borrowed")
