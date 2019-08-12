from django.urls import path

from . import views

urlpatterns = [
        # path('', views.index, name='index'),
        path('', views.IndexView.as_view(), name='index'),
        path('form/<slug:location_name_slug>/', views.form_budget, name='form_budget'),

        ### Budget by Customer by Plant ###
        path('budget/customer-plant/', views.ChooseCustomerBudgetCustomerPlant.as_view(), name='cc_budget_customer_plant'),
        path('budget/customer-plant/<slug:customer_name_slug>/', views.ChooseYearBudgetCustomerPlant.as_view(), name='cy_budget_customer_plant'),
        path('budget/customer-plant/<slug:customer_name_slug>/<int:year>/', views.budget_customer_plant, name='budget_customer_plant'),

        ### Budget by Plant by Customer ###
        path('budget/plant-customer/', views.ChooseLocationBudgetPlantCustomer.as_view(), name='cl_budget_plant_customer'),
        path('budget/plant-customer/<slug:location_name_slug>', views.ChooseYearBudgetPlantCustomer.as_view(), name='cy_budget_plant_customer'),
        path('budget/plant-customer/<slug:location_name_slug>/<int:year>', views.budget_plant_customer, name='budget_plant_customer'),
        
        ### Budget by Plant by Sector ###
        path('budget/plant-sector/', views.ChooseLocationBudgetPlantSector.as_view(), name='cl_budget_plant_sector'),
        path('budget/plant-sector/<slug:location_name_slug>', views.ChooseYearBudgetPlantSector.as_view(), name='cy_budget_plant_sector'),
        path('budget/plant-sector/<slug:location_name_slug>/<int:year>', views.budget_plant_sector, name='budget_plant_sector'),

        ### Budget by Region by Plant ###
        path('budget/region-plant/', views.ChooseLocationBudgetRegionPlant.as_view(), name='cl_budget_region_plant'),
        path('budget/region-plant/<slug:region_name_slug>', views.ChooseYearBudgetRegionPlant.as_view(), name='cy_budget_region_plant'),
        path('budget/region-plant/<slug:region_name_slug>/<int:year>', views.budget_region_plant, name='budget_region_plant'),

        ### Budget by Region by Customer ###
        path('budget/region-customer/', views.ChooseLocationBudgetRegionCustomer.as_view(), name='cl_budget_region_customer'),
        path('budget/region-customer/<slug:region_name_slug>', views.ChooseYearBudgetRegionCustomer.as_view(), name='cy_budget_region_customer'),
        path('budget/region-customer/<slug:region_name_slug>/<int:year>', views.budget_region_customer, name='budget_region_customer'),

        ### Budget by Region by Sector ###
        path('budget/region-sector/', views.ChooseLocationBudgetRegionSector.as_view(), name='cl_budget_region_sector'),
        path('budget/region-sector/<slug:region_name_slug>', views.ChooseYearBudgetRegionSector.as_view(), name='cy_budget_region_sector'),
        path('budget/region-sector/<slug:region_name_slug>/<int:year>', views.budget_region_sector, name='budget_region_sector'),

        ### Global budget by Plant ###
        path('budget/global-plant/', views.ChooseYearBudgetGlobalPlant.as_view(), name='cy_budget_global_plant'),
        path('budget/global-plant/<int:year>', views.budget_global_plant, name='budget_global_plant'),

        ### Global budget by Customer ###
        path('budget/global-customer/', views.ChooseYearBudgetGlobalCustomer.as_view(), name='cy_budget_global_customer'),
        path('budget/global-customer/<int:year>', views.budget_global_customer, name='budget_global_customer'),

        ### Global budget by Sector ###
        path('budget/global-sector/', views.ChooseYearBudgetGlobalSector.as_view(), name='cy_budget_global_sector'),
        path('budget/global-sector/<int:year>', views.budget_global_sector, name='budget_global_sector'),

        ### Global budget by Region ###
        path('budget/global-region/', views.ChooseYearBudgetGlobalRegion.as_view(), name='cy_budget_global_region'),
        path('budget/global-region/<int:year>', views.budget_global_region, name='budget_global_region'),

        ### Sales by Customer by Plant ###
        path('sale/customer-plant/', views.ChooseCustomerSaleCustomerPlant.as_view(), name='cc_sale_customer_plant'),
        path('sale/customer-plant/<slug:customer_name_slug>/', views.ChooseYearSaleCustomerPlant.as_view(), name='cy_sale_customer_plant'),
        path('sale/customer-plant/<slug:customer_name_slug>/<int:year>/', views.sale_customer_plant, name='sale_customer_plant'),

        ### Sales by Plant by Customer ###
        path('sale/plant-customer/', views.ChooseLocationSalePlantCustomer.as_view(), name='cl_sale_plant_customer'),
        path('sale/plant-customer/<slug:location_name_slug>', views.ChooseYearSalePlantCustomer.as_view(), name='cy_sale_plant_customer'),
        path('sale/plant-customer/<slug:location_name_slug>/<int:year>', views.sale_plant_customer, name='sale_plant_customer'),

        ### Sales by Plant by Sector ###
        path('sale/plant-sector/', views.ChooseLocationSalePlantSector.as_view(), name='cl_sale_plant_sector'),
        path('sale/plant-sector/<slug:location_name_slug>', views.ChooseYearSalePlantSector.as_view(), name='cy_sale_plant_sector'),
        path('sale/plant-sector/<slug:location_name_slug>/<int:year>', views.sale_plant_sector, name='sale_plant_sector'),

        ### Sales by Region by Plant ###
        path('sale/region-plant/', views.ChooseLocationSaleRegionPlant.as_view(), name='cl_sale_region_plant'),
        path('sale/region-plant/<slug:region_name_slug>', views.ChooseYearSaleRegionPlant.as_view(), name='cy_sale_region_plant'),
        path('sale/region-plant/<slug:region_name_slug>/<int:year>', views.sale_region_plant, name='sale_region_plant'),

        ### Sales by Region by Customer ###
        path('sale/region-customer/', views.ChooseLocationSaleRegionCustomer.as_view(), name='cl_sale_region_customer'),
        path('sale/region-customer/<slug:region_name_slug>', views.ChooseYearSaleRegionCustomer.as_view(), name='cy_sale_region_customer'),
        path('sale/region-customer/<slug:region_name_slug>/<int:year>', views.sale_region_customer, name='sale_region_customer'),

        ### Sales by Region by Sector ###
        path('sale/region-sector/', views.ChooseLocationSaleRegionSector.as_view(), name='cl_sale_region_sector'),
        path('sale/region-sector/<slug:region_name_slug>', views.ChooseYearSaleRegionSector.as_view(), name='cy_sale_region_sector'),
        path('sale/region-sector/<slug:region_name_slug>/<int:year>', views.sale_region_sector, name='sale_region_sector'),

        ### Global sales by Plant ###
        path('sale/global-plant/', views.ChooseYearSaleGlobalPlant.as_view(), name='cy_sale_global_plant'),
        path('sale/global-plant/<int:year>', views.sale_global_plant, name='sale_global_plant'),
        
        ### Global sales by Customer ###
        path('sale/global-customer/', views.ChooseYearSaleGlobalCustomer.as_view(), name='cy_sale_global_customer'),
        path('sale/global-customer/<int:year>', views.sale_global_customer, name='sale_global_customer'),

        ### Global sales by Sector ###
        path('sale/global-sector/', views.ChooseYearSaleGlobalSector.as_view(), name='cy_sale_global_sector'),
        path('sale/global-sector/<int:year>', views.sale_global_sector, name='sale_global_sector'),

        ### Global sales by Region ###
        path('sale/global-region/', views.ChooseYearSaleGlobalRegion.as_view(), name='cy_sale_global_region'),
        path('sale/global-region/<int:year>', views.sale_global_region, name='sale_global_region'),
]
