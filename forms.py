from django import forms

TYPE_CHOICES = [
    ('plant-customer', 'Sales by Plant by Customer'),
    ('plant-sector', 'Sales by Plant by Sector'),
    ('region-plant', 'Sales by Region by Plant'),
    ('region-customer', 'Sales by Region by Customer'),
    ('region-sector', 'Sales by Region by Sector'),
    ('global-plant', 'Global sales by Plant'),
    ('global-customer', 'Global sales by Customer'),
    ('global-sector', 'Global sales by Sector'),
    ('global-region', 'Global sales by Region'),
]

class BudgetTypeForm(forms.Form):
    budget_type = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control mb-3 w-25 mx-auto'}),
        choices=TYPE_CHOICES,
    )
    year = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control mb-3 w-25 mx-auto'}),
        choices=[
            ('2019', '2019'),
        ]
    )