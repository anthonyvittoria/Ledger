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