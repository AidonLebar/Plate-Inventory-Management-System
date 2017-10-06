import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import InventoryItem, Order, OrderItem

class InventoryItemModelTest(TestCase):

    def test_name_string(self):
        """
        The name of the item should be returned by __str__().
        """
        name = "test"
        stock = 50
        i = InventoryItem(item_name = name, total_stock = stock)
        self.assertEquals(str(i), name)

class OrderModelTest(TestCase):

    def test_string(self):
        """
        The name of the borrower and the start date of the order should be returned by __str__().
        """
        name = "testOrder"
        start = timezone.now()
        start_trunc = start.strftime('%Y-%m-%d')
        end = timezone.now() + datetime.timedelta(days = 1)
        o = Order(borrower_name = name, start_time = start, end_time = end)
        self.assertEquals(str(o), name + ' : ' + start_trunc)

    def test_active_order_with_active_order(self):
        """
        Order should be active when current time is between start and end time of order.
        """
        name = "testOrder"
        time = timezone.now()
        start = timezone.now() - datetime.timedelta(days = 1)
        end = timezone.now() + datetime.timedelta(days = 1)
        activeOrder = Order(borrower_name = name, start_time = start, end_time = end)
        self.assertIs(activeOrder.activeOrder(), True)

    def test_active_order_with_pre_active_order(self):
        """
        Order should be inactive when current time is before start time of order.
        """
        name = "tetsOrder"
        time = timezone.now()
        start = timezone.now() + datetime.timedelta(days = 1)
        end = timezone.now() + datetime.timedelta(days = 2)
        activeOrder = Order(borrower_name = name, start_time = start, end_time = end)
        self.assertIs(activeOrder.activeOrder(), False)

    def test_active_order_with_post_active_order(self):
        """
        Order should be inactive when current time is after end time of order.
        """
        name = "testOrder"
        time = timezone.now()
        start = timezone.now() - datetime.timedelta(days = 2)
        end = timezone.now() - datetime.timedelta(days = 1)
        activeOrder = Order(borrower_name = name, start_time = start, end_time = end)
        self.assertIs(activeOrder.activeOrder(), False)

    def test_end_time_before_start_time(self):
        """
        A ValidationError should be raised if the order's end time is before start time.
        """
        name = "testOrder"
        start = timezone.now()
        end = timezone.now() - datetime.timedelta(days = 1)
        o = Order(borrower_name = name, start_time = start, end_time = end)
        self.assertRaises(ValidationError)

    def test_no_start_time(self):
        """
        A ValidationError should be raised if there is no start time on the order.
        """

        name = "testOrder"
        end = timezone.now() - datetime.timedelta(days = 1)
        o = Order(borrower_name = name, end_time = end)
        self.assertRaises(ValidationError)

    def test_no_end_time(self):
        """
        A ValidationError should be raised if there is no end time to the order.
        """
        name = "test"
        start = timezone.now() - datetime.timedelta(days = 1)
        o = Order(borrower_name = name, start_time = start)
        self.assertRaises(ValidationError)

class OrderItemModelTest(TestCase):

    def test_string(self):
        """
        Order item's quantity and name should be returned by __str__() in format.
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
        Item delta or loss should be the difference between amount borrowed and amount returned.
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
        A ValidationError should be raised if no quantity_borrowed is given
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
        A ValidationError should be raised if quantity_borrowed is 0.
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
        A ValidationError should be raised if quantity_returned is greater than quantity_borrowed.
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
        Order item should be active if it's order is active.
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
        Order item should should be inactive if current time is before it's order's start time.
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
        Order item should be inactive if current time is after it's order's end time.
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
