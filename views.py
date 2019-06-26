from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader

from .models import Sale

def index(request):
    latest_sales_list = Sale.objects.order_by('id')[:25]
    template = loader.get_template('SalesQuery/index.html')
    context = {
            'latest_sales_list': latest_sales_list,
    }
    return HttpResponse(template.render(context, request))