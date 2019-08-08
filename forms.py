from django import forms

from . import models

class BudgetForm(forms.ModelForm):
    class Meta:
        model = models.Budget
        fields = [
            'customer',
            'jan', 'feb', 'mar', 'apr',
            'may', 'jun', 'jul', 'aug',
            'sep', 'oct', 'nov', 'dec',
            'year',
        ]

BudgetFormSet = forms.inlineformset_factory(
    models.Location,
    models.Budget,
    extra=1,
    fields=(
        'year', 'customer',
        'jan', 'feb', 'mar', 'apr',
        'may', 'jun', 'jul', 'aug',
        'sep', 'oct', 'nov', 'dec',
    ),
    min_num=4,
)