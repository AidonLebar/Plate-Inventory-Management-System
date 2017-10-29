from django import forms

QUICK_ORDER_CHOICES =(
                ('Plate', 'Plate'),
                ('Bowl', 'Bowl'),
                ('Spoon', 'Spoon'),
                ('Fork', 'Fork'),
                )


class quickOrderForm(forms.Form):
    name = forms.CharField(label=False, max_length=100)
    items = forms.MultipleChoiceField(label=False, widget=forms.CheckboxSelectMultiple, choices=QUICK_ORDER_CHOICES)
