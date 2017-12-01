from django import forms
from django.core.validators import MinValueValidator
import datetime
from .models import InventoryItem

class quickOrderForm(forms.Form):
    """
    Form for quick add sidebar.
    """

    name = forms.CharField(label=False, max_length=100)
    items = forms.ModelMultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple(), queryset=InventoryItem.objects.filter(quick_order_item=True))

class addItemForm(forms.Form):
    """
    Form for Adding new items to inventory.
    """

    item_name = forms.CharField(label='Item Name', max_length=100)
    stock = forms.IntegerField(validators=[MinValueValidator(1)])
    quick_order_item = forms.BooleanField(label='Quick Order Item', required=False)

class orderForm(forms.Form):
    """
    Form for placing a new order.
    """

    borrower_name = forms.CharField(label='Borrower Name', max_length=100)
    start_time = forms.DateTimeField(label='Start Date and Time', initial=datetime.date.today)
    end_time = forms.DateTimeField(label='End Date and Time', initial=datetime.date.today)

class returnItemForm(forms.Form):
    """
    Form for returning individual items in a order.
    """

    returned = forms.IntegerField(validators=[MinValueValidator(0)],label=False)

class addOrderItemForm(forms.Form):
    """
    Form for adding a new item to an order.
    """

    item_queryset = InventoryItem.objects.all() #placeholder edited by view
    item_to_add = forms.ModelChoiceField(required=True, queryset=item_queryset)
    quantity_to_borrow = forms.IntegerField(validators=[MinValueValidator(1)],label=False)

class editItemForm(forms.Form):
    """
    Form for editing the name or stock of an item in the inventory.
    """

    stock = 1 #placeholder default replaced by view
    new_name = forms.CharField(label='Item Name', max_length=100, initial = "")
    new_total_stock = forms.IntegerField(validators=[MinValueValidator(1)],label='Total Stock', initial = stock)
    quick_order_item = forms.BooleanField(label='Quick Order Item', required=False)

class editOrderForm(forms.Form):
    """
    Form for editing borrower, start time or end time of an order.
    """

    new_borrower = forms.CharField(label="Borrower's Name", max_length=100, initial = "")
    new_start_time = forms.DateTimeField(label='Start Date and Time', initial=datetime.date.today)
    new_end_time = forms.DateTimeField(label='End Date and Time', initial=datetime.date.today)

class editOrderItemForm(forms.Form):
    """
    Form for editing the quantity of an order item.
    """

    quantity = forms.IntegerField(validators=[MinValueValidator(1)],label=False)
