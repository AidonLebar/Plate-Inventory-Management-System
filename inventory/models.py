import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.db import models

class InventoryItem(models.Model):
    item_name = models.CharField(max_length = 100)
    total_stock = models.PositiveIntegerField()

    def __str__(self):
        """
        Does nothing, returns inventory item name as string.
        """
        return self.item_name

    def currentStock(self):
        """
        Calculates current stock as total stock minus what is currently out in active orders, returns an integer.
        """
        stock = self.total_stock
        for  i in self.orderitem_set.all():
            if i.activeOrderItem():
                stock = stock - i.quantity_borrowed
        return stock

    def clean(self):
          """
          Ensures total stock is not 0. Returns nothing, but raises exceptions
          """
          if self.total_stock == 0:
              raise ValidationError("Total stock must be a non-zero quantity")

    def averageOrder(self):
        """
        Calculates mean of orders of specific item type, returns a float.
        """
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
        """
        Does nothing, returns borrowers name and start date as a string.
        """
        start_date = self.start_time.strftime('%Y-%m-%d')
        return '{} : {}'.format(self.borrower_name, start_date)

    def activeOrder(self):
        """
        Determines if order is active if current time is between order start time and end time, returns a boolean.
        """
        now = timezone.now()
        return (now >= self.start_time) and (now <= self.end_time)

    def clean(self):
        """
        Ensures datetme fields are filled and that the end time is not before the start time.
        Returns nothing, but will raise exceptions.
        """
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
        """
        Does nothing, returns quantity borrowed and item name as a string.
        """
        return '{} {}'.format(self.quantity_borrowed, self.item.item_name)

    def activeOrderItem(self):
        """
        Determines if order item is active using the active status of its corresponsing order.
        returns a boolean.
        """
        return self.order.activeOrder();

    def itemDelta(self):
        """
        Determines loss as difference between quantity borrwed and quantity returned, returns an integer.
        """
        return self.quantity_borrowed - self.quantity_returned

    def clean(self):
        """
        Ensures quantity borrowed is not 0 or None, and ensure quantity returne is not greater than quantity borrowed.
        Returns nothing, but will raise exceptions.
        """
        if self.quantity_borrowed == 0 or self.quantity_borrowed is None:
            raise ValidationError("Order item must have a quantity")

        if self.quantity_returned > self.quantity_borrowed:
            raise ValidationError("Cannot return more than was borrowed")

        inventory_during_order = self.item.total_stock
        for e in Order.objects.all():
            if not(((e.start_time > self.order.end_time))or((e.end_time < self.order.start_time))):
                for i in e.orderitem_set.all():
                    if i.item.item_name == self.item.item_name:
                        inventory_during_order -= i.quantity_borrowed


        if self.quantity_borrowed > inventory_during_order:
            raise ValidationError("Cannot borrow more than available, there are %i %s available at this time" % (inventory_during_order, self.item.item_name))
