from django import forms
from django.core.validators import MinValueValidator

class quickOrderForm(forms.Form):
    QUICK_ORDER_CHOICES =(
                    ('Plate', 'Plate'),
                    ('Bowl', 'Bowl'),
                    ('Spoon', 'Spoon'),
                    ('Fork', 'Fork'),
                    )

    name = forms.CharField(label=False, max_length=100)
    items = forms.MultipleChoiceField(label=False, widget=forms.CheckboxSelectMultiple, choices=QUICK_ORDER_CHOICES)

class addItemForm(forms.Form):
    item_name = forms.CharField(label='Item Name', max_length=100)
    stock = forms.IntegerField(validators=[MinValueValidator(1)])
