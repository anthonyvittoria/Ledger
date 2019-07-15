from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('sale/', views.choose_sale, name='choose_sale'),
        path('sale/location/<slug:location_name_slug>', views.sale_by_location, name='sale_by_location'),
        path('sale/customer/<slug:customer_name_slug>', views.sale_by_customer, name='sale_by_customer'),
        path('budget/plant-customer/', views.cl_budget_plant_customer, name='cl_budget_plant_customer'),
        path('budget/plant-customer/<slug:location_name_slug>', views.cy_budget_plant_customer, name='cy_budget_plant_customer'),
        path('budget/<slug:location_name_slug>/<int:year>', views.budget_plant_customer, name='budget_plant_customer'),
]
