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
        name = "test"
        start = timezone.now()
        start_trunc = start.strftime('%Y-%m-%d')
        end = timezone.now() + datetime.timedelta(days = 1)
        o = Order(borrower_name = name, start_time = start, end_time = end)
        self.assertEquals(str(o), name + ' : ' + start_trunc)

    def test_active_order_with_active_order(self):
        """
        activeOrder() returns true for an order when current time is between start and end time of order
        """
        time = timezone.now()
        start = timezone.now() - datetime.timedelta(days = 1)
        end = timezone.now() + datetime.timedelta(days = 1)
        activeOrder = Order(borrower_name = 'test', start_time = start, end_time = end)
        self.assertIs(activeOrder.activeOrder(), True)

    def test_active_order_with_pre_active_order(self):
        """
        activeOrder() returns false for an order when current time is before start time of order
        """
        time = timezone.now()
        start = timezone.now() + datetime.timedelta(days = 1)
        end = timezone.now() + datetime.timedelta(days = 2)
        activeOrder = Order(borrower_name = 'test', start_time = start, end_time = end)
        self.assertIs(activeOrder.activeOrder(), False)

    def test_active_order_with_post_active_order(self):
        """
        activeOrder() returns false for an order when current time is after end time of order
        """
        time = timezone.now()
        start = timezone.now() - datetime.timedelta(days = 2)
        end = timezone.now() - datetime.timedelta(days = 1)
        activeOrder = Order(borrower_name = 'test', start_time = start, end_time = end)
        self.assertIs(activeOrder.activeOrder(), False)

    def test_end_time_before_start_time(self):
        """
        ValidationError should be raised if end time is before start time
        """
        name = "test"
        start = timezone.now()
        end = timezone.now() - datetime.timedelta(days = 1)
        o = Order(borrower_name = name, start_time = start, end_time = end)
        self.assertRaises(ValidationError)

    def test_no_start_time(self):
        """
        ValidationError should be raised if there is no start time
        """

        name = "test"
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
