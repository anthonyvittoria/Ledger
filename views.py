from django.shortcuts import get_object_or_404, render
from django.template import loader

from .models import Budget, Sale, Location

def choose_budget(request):

    budget_locations = []

    for budget in Budget.objects.all():
        if budget not in budget_locations:
            budget_locations.append(budget.location)

    locations = Location.objects.filter(name__in=budget_locations)

    context = {
        'locations': locations,
    }
    return render(request, 'SalesQuery/choosebudget.html', context)

def index(request):
    latest_sales_list = Sale.objects.order_by('id')[:25]
    
    context = {
        'latest_sales_list': latest_sales_list,
    }
    return render(request, 'SalesQuery/index.html', context)

def budget(request, location_name_slug):
    budget_objects = Budget.objects.filter(location__slug=location_name_slug)
    location = budget_objects[0].location
    year = budget_objects[0].year
    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    budget_total, cust_total = 0, 0

    for budget in budget_objects:
        jan_total += budget.jan
        feb_total += budget.feb
        mar_total += budget.mar
        apr_total += budget.apr
        may_total += budget.may
        jun_total += budget.jun
        jul_total += budget.jul
        aug_total += budget.aug
        sep_total += budget.sep
        oct_total += budget.oct
        nov_total += budget.nov
        dec_total += budget.dec
        q1_total += budget.q1
        q2_total += budget.q2
        q3_total += budget.q3
        q4_total += budget.q4
        budget_total += (budget.q1 + budget.q2 + budget.q3 + budget.q4)

    context = {
        'budget_objects': budget_objects,
        'location': location,
        'year': year,
        'jan_total': jan_total,
        'feb_total': feb_total,
        'mar_total': mar_total,
        'apr_total': apr_total,
        'may_total': may_total,
        'jun_total': jun_total,
        'jul_total': jul_total,
        'aug_total': aug_total,
        'sep_total': sep_total,
        'oct_total': oct_total,
        'nov_total': nov_total,
        'dec_total': dec_total,
        'q1_total': q1_total,
        'q2_total': q2_total,
        'q3_total': q3_total,
        'q4_total': q4_total,
        'budget_total': budget_total,
    }
    return render(request, 'SalesQuery/budget.html', context)