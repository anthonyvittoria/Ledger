from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader

from .models import Budget, Sale, Location

def choose_budget(request):

    budget_locations = []

    for budget in Budget.objects.all():
        if budget not in budget_locations:
            budget_locations.append(budget.location)

    locations = Location.objects.filter(name__in=budget_locations)

    template = loader.get_template('SalesQuery/choosebudget.html')
    
    context = {
        'locations': locations,
    }
    return HttpResponse(template.render(context, request))

def index(request):
    latest_sales_list = Sale.objects.order_by('id')[:25]
    
    template = loader.get_template('SalesQuery/index.html')
    
    context = {
        'latest_sales_list': latest_sales_list,
    }
    return HttpResponse(template.render(context, request))

def budget(request, location):
    budget_objects = Budget.objects.filter(location=location)
    q1 = current_budget.jan + current_budget.feb + current_budget.mar
    q2 = current_budget.apr + current_budget.may + current_budget.jun
    q3 = current_budget.jul + current_budget.aug + current_budget.sep
    q4 = current_budget.oct + current_budget.nov + current_budget.dec

    template = loader.get_template('SalesQuery/budget.html')

    context = {
        'budget_objects': budget_objects,
        'q1': q1,
        'q2': q2,
        'q3': q3,
        'q4': q4,
    }
    return HttpResponse(template.render(context, request))