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

BudgetFormSet = forms.modelformset_factory(
    model=models.Budget,
    form=BudgetForm,
)