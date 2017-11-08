from django import forms
from django.core.validators import MinValueValidator
import datetime
from .models import InventoryItem

class quickOrderForm(forms.Form):
    QUICK_ORDER_CHOICES =(
                    ('Plate', 'Plate'),
                    ('Bowl', 'Bowl'),
                    ('Spoon', 'Spoon'),
                    ('Fork', 'Fork'),
                    )

    name = forms.CharField(label=False, max_length=100)
    items = forms.MultipleChoiceField(label=False, widget=forms.CheckboxSelectMultiple(attrs={'class':'quick_order_form_checkboxes'}), choices=QUICK_ORDER_CHOICES)

class addItemForm(forms.Form):
    item_name = forms.CharField(label='Item Name', max_length=100)
    stock = forms.IntegerField(validators=[MinValueValidator(1)])

class orderForm(forms.Form):
    borrower_name = forms.CharField(label='Borrower Name', max_length=100)
    start_time = forms.DateTimeField(label='Start Date and Time', initial=datetime.date.today)
    end_time = forms.DateTimeField(label='End Date and Time', initial=datetime.date.today)

class returnItemForm(forms.Form):
    returned = forms.IntegerField(validators=[MinValueValidator(0)],label=False)

class addOrderItemForm(forms.Form):
    item_queryset = InventoryItem.objects.all()
    item_to_add = forms.ModelChoiceField(required=True, queryset=item_queryset)
    quantity_to_borrow = forms.IntegerField(validators=[MinValueValidator(1)],label=False)

class editItemForm(forms.Form):
    stock = 1
    new_name = forms.CharField(label='Item Name', max_length=100, initial = "")
    new_total_stock = forms.IntegerField(validators=[MinValueValidator(1)],label='Total Stock', initial = stock)

class editOrderForm(forms.Form):
    new_borrower = forms.CharField(label="Borrower's Name", max_length=100, initial = "")
    new_start_time = forms.DateTimeField(label='Start Date and Time', initial=datetime.date.today)
    new_end_time = forms.DateTimeField(label='End Date and Time', initial=datetime.date.today)
