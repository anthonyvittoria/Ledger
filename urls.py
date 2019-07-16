from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        ### Budget by Plant by Customer ###
        path('budget/plant-customer/', views.cl_budget_plant_customer, name='cl_budget_plant_customer'),
        path('budget/plant-customer/<slug:location_name_slug>', views.cy_budget_plant_customer, name='cy_budget_plant_customer'),
        path('budget/plant-customer/<slug:location_name_slug>/<int:year>', views.budget_plant_customer, name='budget_plant_customer'),
        
        ### Budget by Plant by Sector ###
        path('budget/plant-sector/', views.cl_budget_plant_sector, name='cl_budget_plant_sector'),
        path('budget/plant-sector/<slug:location_name_slug>', views.cy_budget_plant_sector, name='cy_budget_plant_sector'),
        path('budget/plant-sector/<slug:location_name_slug>/<int:year>', views.budget_plant_sector, name='budget_plant_sector'),

        ### Budget by Region by Plant ###
        path('budget/region-plant/', views.cl_budget_region_plant, name='cl_budget_region_plant'),
        path('budget/region-plant/<slug:region_name_slug>', views.cy_budget_region_plant, name='cy_budget_region_plant'),
        path('budget/region-plant/<slug:region_name_slug>/<int:year>', views.budget_region_plant, name='budget_region_plant'),

        ### Budget by Region by Customer ###
        path('budget/region-customer/', views.cl_budget_region_customer, name='cl_budget_region_customer'),
        path('budget/region-customer/<slug:region_name_slug>', views.cy_budget_region_customer, name='cy_budget_region_customer'),
        path('budget/region-customer/<slug:region_name_slug>/<int:year>', views.budget_region_customer, name='budget_region_customer'),
]
