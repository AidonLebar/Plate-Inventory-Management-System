import datetime

from django.utils import timezone
from django.test import TestCase

from .models import InventoryItem, Order, OrderItem

class OrderModelTest(TestCase):

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
