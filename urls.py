from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('form/<slug:location_name_slug>', views.form_budget, name='form_budget'),

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

        ### Budget by Region by Sector ###
        path('budget/region-sector/', views.cl_budget_region_sector, name='cl_budget_region_sector'),
        path('budget/region-sector/<slug:region_name_slug>', views.cy_budget_region_sector, name='cy_budget_region_sector'),
        path('budget/region-sector/<slug:region_name_slug>/<int:year>', views.budget_region_sector, name='budget_region_sector'),

        ### Global budget by Plant ###
        path('budget/global-plant/', views.cy_budget_global_plant, name='cy_budget_global_plant'),
        path('budget/global-plant/<int:year>', views.budget_global_plant, name='budget_global_plant'),

        ### Global budget by Customer ###
        path('budget/global-customer/', views.cy_budget_global_customer, name='cy_budget_global_customer'),
        path('budget/global-customer/<int:year>', views.budget_global_customer, name='budget_global_customer'),

        ### Global budget by Sector ###
        path('budget/global-sector/', views.cy_budget_global_sector, name='cy_budget_global_sector'),
        path('budget/global-sector/<int:year>', views.budget_global_sector, name='budget_global_sector'),

        ### Global budget by Sector ###
        path('budget/global-region/', views.cy_budget_global_region, name='cy_budget_global_region'),
        path('budget/global-region/<int:year>', views.budget_global_region, name='budget_global_region'),

        ### Sales by Plant by Customer ###
        path('sale/plant-customer/', views.cl_sale_plant_customer, name='cl_sale_plant_customer'),
        path('sale/plant-customer/<slug:location_name_slug>', views.cy_sale_plant_customer, name='cy_sale_plant_customer'),
        path('sale/plant-customer/<slug:location_name_slug>/<int:year>', views.sale_plant_customer, name='sale_plant_customer'),

        ### Sales by Plant by Sector ###
        path('sale/plant-sector/', views.cl_sale_plant_sector, name='cl_sale_plant_sector'),
        path('sale/plant-sector/<slug:location_name_slug>', views.cy_sale_plant_sector, name='cy_sale_plant_sector'),
        path('sale/plant-sector/<slug:location_name_slug>/<int:year>', views.sale_plant_sector, name='sale_plant_sector'),

        ### Sales by Region by Plant ###
        path('sale/region-plant/', views.cl_sale_region_plant, name='cl_sale_region_plant'),
        path('sale/region-plant/<slug:region_name_slug>', views.cy_sale_region_plant, name='cy_sale_region_plant'),
        path('sale/region-plant/<slug:region_name_slug>/<int:year>', views.sale_region_plant, name='sale_region_plant'),

        ### Sales by Region by Customer ###
        path('sale/region-customer/', views.cl_sale_region_customer, name='cl_sale_region_customer'),
        path('sale/region-customer/<slug:region_name_slug>', views.cy_sale_region_customer, name='cy_sale_region_customer'),
        path('sale/region-customer/<slug:region_name_slug>/<int:year>', views.sale_region_customer, name='sale_region_customer'),

        ### Sales by Region by Sector ###
        path('sale/region-sector/', views.cl_sale_region_sector, name='cl_sale_region_sector'),
        path('sale/region-sector/<slug:region_name_slug>', views.cy_sale_region_sector, name='cy_sale_region_sector'),
        path('sale/region-sector/<slug:region_name_slug>/<int:year>', views.sale_region_sector, name='sale_region_sector'),

        ### Global sales by Plant ###
        path('sale/global-plant/', views.cy_sale_global_plant, name='cy_sale_global_plant'),
        path('sale/global-plant/<int:year>', views.sale_global_plant, name='sale_global_plant'),
        
        ### Global sales by Customer ###
        path('sale/global-customer/', views.cy_sale_global_customer, name='cy_sale_global_customer'),
        path('sale/global-customer/<int:year>', views.sale_global_customer, name='sale_global_customer'),

        ### Global sales by Sector ###
        path('sale/global-sector/', views.cy_sale_global_sector, name='cy_sale_global_sector'),
        path('sale/global-sector/<int:year>', views.sale_global_sector, name='sale_global_sector'),

        ### Global sales by Region ###
        path('sale/global-region/', views.cy_sale_global_region, name='cy_sale_global_region'),
        path('sale/global-region/<int:year>', views.sale_global_region, name='sale_global_region'),
]
