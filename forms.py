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
    models.Budget,
    form=BudgetForm,
)

BudgetInlineFormSet = forms.inlineformset_factory(
    models.Location,
    models.Budget,
    extra=1,
    fields=(
        'customer',
        'jan', 'feb', 'mar', 'apr',
        'may', 'jun', 'jul', 'aug',
        'sep', 'oct', 'nov', 'dec',
        'year',
    ),
    formset=BudgetFormSet,
    min_num=4,
)