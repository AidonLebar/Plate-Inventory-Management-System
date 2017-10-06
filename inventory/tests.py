import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import InventoryItem, Order, OrderItem

class InventoryItemTest(TestCase):

    def test_name_string(self):
        """
        __str__() should return the name of the item
        """
        name = "test"
        stock = 50
        i = InventoryItem(item_name = name, total_stock = stock)
        self.assertEquals(str(i), name)

class OrderModelTest(TestCase):

    def test_string(self):
        """
        ___str__() should return the name of the borrower an the start date
        """
        name = "testOrder"
        start = timezone.now()
        start_trunc = start.strftime('%Y-%m-%d')
        end = timezone.now() + datetime.timedelta(days = 1)
        o = Order(borrower_name = name, start_time = start, end_time = end)
        self.assertEquals(str(o), name + ' : ' + start_trunc)

    def test_active_order_with_active_order(self):
        """
        activeOrder() returns true for an order when current time is between start and end time of order
        """
        name = "testOrder"
        time = timezone.now()
        start = timezone.now() - datetime.timedelta(days = 1)
        end = timezone.now() + datetime.timedelta(days = 1)
        activeOrder = Order(borrower_name = name, start_time = start, end_time = end)
        self.assertIs(activeOrder.activeOrder(), True)

    def test_active_order_with_pre_active_order(self):
        """
        activeOrder() returns false for an order when current time is before start time of order
        """
        name = "tetsOrder"
        time = timezone.now()
        start = timezone.now() + datetime.timedelta(days = 1)
        end = timezone.now() + datetime.timedelta(days = 2)
        activeOrder = Order(borrower_name = name, start_time = start, end_time = end)
        self.assertIs(activeOrder.activeOrder(), False)

    def test_active_order_with_post_active_order(self):
        """
        activeOrder() returns false for an order when current time is after end time of order
        """
        name = "testOrder"
        time = timezone.now()
        start = timezone.now() - datetime.timedelta(days = 2)
        end = timezone.now() - datetime.timedelta(days = 1)
        activeOrder = Order(borrower_name = name, start_time = start, end_time = end)
        self.assertIs(activeOrder.activeOrder(), False)

    def test_end_time_before_start_time(self):
        """
        ValidationError should be raised if end time is before start time
        """
        name = "testOrder"
        start = timezone.now()
        end = timezone.now() - datetime.timedelta(days = 1)
        o = Order(borrower_name = name, start_time = start, end_time = end)
        self.assertRaises(ValidationError)

    def test_no_start_time(self):
        """
        ValidationError should be raised if there is no start time
        """

        name = "testOrder"
        end = timezone.now() - datetime.timedelta(days = 1)
        o = Order(borrower_name = name, end_time = end)
        self.assertRaises(ValidationError)

    def test_no_end_time(self):
        """
        ValidationError should be raised if there is no end time
        """
        name = "test"
        start = timezone.now() - datetime.timedelta(days = 1)
        o = Order(borrower_name = name, start_time = start)
        self.assertRaises(ValidationError)

class OrderItemTest(TestCase):

    def test_string(self):
        """
        ___str__() should return quantity and name of order item
        """
        name = "testItem"
        testStock = 500
        i = InventoryItem(item_name = name, total_stock = testStock)

        orderName = "testOrder"
        start = timezone.now() - datetime.timedelta(days = 1)
        end = timezone.now() + datetime.timedelta(days = 1)
        o = Order(borrower_name = orderName, start_time = start, end_time = end)

        testQuantity = 50
        oi = OrderItem(order = o, item = i, quantity_borrowed = testQuantity)

        self.assertEquals(str(oi), str(testQuantity) + ' ' + name)

    def test_item_delta(self):
        """
        itemDelta() should return the difference between amount borrowed and ammount returned
        """
        name = "testItem"
        testStock = 500
        i = InventoryItem(item_name = name, total_stock = testStock)

        orderName = "testOrder"
        start = timezone.now() - datetime.timedelta(days = 1)
        end = timezone.now() + datetime.timedelta(days = 1)
        o = Order(borrower_name = orderName, start_time = start, end_time = end)

        testQuantity = 50
        testReturnQuantity = 20
        oi = OrderItem(order = o, item = i, quantity_borrowed = testQuantity, quantity_returned = testReturnQuantity)

        self.assertEquals(oi.itemDelta(), testQuantity - testReturnQuantity)

    def test_quantity_borrowed_equals_None(self):
        """
        clean() should raise ValidationError if no quantity_borrowed is given
        """
        name = "testItem"
        testStock = 500
        i = InventoryItem(item_name = name, total_stock = testStock)

        orderName = "testOrder"
        start = timezone.now() - datetime.timedelta(days = 1)
        end = timezone.now() + datetime.timedelta(days = 1)
        o = Order(borrower_name = orderName, start_time = start, end_time = end)

        oi = OrderItem(order = o, item = i)

        self.assertRaises(ValidationError)

    def test_quantity_borrowed_equals_zero(self):
        """
        clean() should raise ValidationError if quantity_borrowed is 0
        """
        name = "testItem"
        testStock = 500
        i = InventoryItem(item_name = name, total_stock = testStock)

        orderName = "testOrder"
        start = timezone.now() - datetime.timedelta(days = 1)
        end = timezone.now() + datetime.timedelta(days = 1)
        o = Order(borrower_name = orderName, start_time = start, end_time = end)

        oi = OrderItem(order = o, item = i, quantity_borrowed = 0)

        self.assertRaises(ValidationError)

    def test_quantity_returned_greater_than_quantity_borrowed(self):
        """
        clean() should raise ValidationError if quantity_returned > quantity_borrowed
        """
        name = "testItem"
        testStock = 500
        i = InventoryItem(item_name = name, total_stock = testStock)

        orderName = "testOrder"
        start = timezone.now() - datetime.timedelta(days = 1)
        end = timezone.now() + datetime.timedelta(days = 1)
        o = Order(borrower_name = orderName, start_time = start, end_time = end)

        borrowed = 10
        returned = 20
        oi = OrderItem(order = o, item = i, quantity_borrowed = borrowed, quantity_returned = returned)

        self.assertRaises(ValidationError)

    def test_active_order_with_active_order(self):
        """
        activeOrderItem() should return true if it's order is active
        """
        name = "testItem"
        testStock = 500
        i = InventoryItem(item_name = name, total_stock = testStock)

        orderName = "testOrder"
        start = timezone.now() - datetime.timedelta(days = 1)
        end = timezone.now() + datetime.timedelta(days = 1)
        o = Order(borrower_name = orderName, start_time = start, end_time = end)

        borrowed = 10
        oi = OrderItem(order = o, item = i, quantity_borrowed = borrowed)

        self.assertIs(oi.activeOrderItem(), True)

    def test_active_order_with_pre_active_order(self):
        """
        activeOrderItem() should return true if now is before it's order's start time
        """
        name = "testItem"
        testStock = 500
        i = InventoryItem(item_name = name, total_stock = testStock)

        orderName = "testOrder"
        start = timezone.now() + datetime.timedelta(days = 1)
        end = timezone.now() + datetime.timedelta(days = 2)
        o = Order(borrower_name = orderName, start_time = start, end_time = end)

        borrowed = 10
        oi = OrderItem(order = o, item = i, quantity_borrowed = borrowed)

        self.assertIs(oi.activeOrderItem(), False)

    def test_active_order_with_post_active_order(self):
        """
        activeOrderItem() should return true if now is after it's order's end time
        """
        name = "testItem"
        testStock = 500
        i = InventoryItem(item_name = name, total_stock = testStock)

        orderName = "testOrder"
        start = timezone.now() - datetime.timedelta(days = 2)
        end = timezone.now() - datetime.timedelta(days = 1)
        o = Order(borrower_name = orderName, start_time = start, end_time = end)

        borrowed = 10
        oi = OrderItem(order = o, item = i, quantity_borrowed = borrowed)

        self.assertIs(oi.activeOrderItem(), False)
