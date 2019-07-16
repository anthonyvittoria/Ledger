from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('budget/plant-customer/', views.cl_budget_plant_customer, name='cl_budget_plant_customer'),
        path('budget/plant-customer/<slug:location_name_slug>', views.cy_budget_plant_customer, name='cy_budget_plant_customer'),
        path('budget/plant-customer/<slug:location_name_slug>/<int:year>', views.budget_plant_customer, name='budget_plant_customer'),
        path('budget/plant-sector/', views.cl_budget_plant_sector, name='cl_budget_plant_sector'),
        path('budget/plant-sector/<slug:location_name_slug>', views.cy_budget_plant_sector, name='cy_budget_plant_sector'),
        path('budget/plant-sector/<slug:location_name_slug>/<int:year>', views.budget_plant_sector, name='budget_plant_sector'),
]
