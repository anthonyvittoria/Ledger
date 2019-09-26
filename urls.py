from django.urls import path

from . import views

urlpatterns = [
        # path('', views.index, name='index'),
        path('', views.IndexView.as_view(), name='index'),
        path('form/', views.BudgetFormChooseLocation.as_view(), name='cl_budget_form'),
        path('form/<slug:location_name_slug>/', views.form_budget, name='budget_form'),

        ### Budget by Customer by Plant ###
        path('budget/customer-plant/', views.ChooseCustomerBudgetCustomerPlant.as_view(), name='cc_budget_customer_plant'),
        path('budget/customer-plant/<slug:customer_name_slug>/', views.ChooseYearBudgetCustomerPlant.as_view(), name='cy_budget_customer_plant'),
        path('budget/customer-plant/<slug:customer_name_slug>/<int:year>/', views.BudgetCustomerPlant.as_view(), name='budget_customer_plant'),

        ### Budget by Plant by Customer ###
        path('budget/plant-customer/', views.ChooseLocationBudgetPlantCustomer.as_view(), name='cl_budget_plant_customer'),
        path('budget/plant-customer/<slug:location_name_slug>', views.ChooseYearBudgetPlantCustomer.as_view(), name='cy_budget_plant_customer'),
        path('budget/plant-customer/<slug:location_name_slug>/<int:year>', views.BudgetPlantCustomer.as_view(), name='budget_plant_customer'),
        
        ### Budget by Plant by Sector ###
        path('budget/plant-sector/', views.ChooseLocationBudgetPlantSector.as_view(), name='cl_budget_plant_sector'),
        path('budget/plant-sector/<slug:location_name_slug>', views.ChooseYearBudgetPlantSector.as_view(), name='cy_budget_plant_sector'),
        path('budget/plant-sector/<slug:location_name_slug>/<int:year>', views.BudgetPlantSector.as_view(), name='budget_plant_sector'),

        ### Budget by Region by Plant ###
        path('budget/region-plant/', views.ChooseLocationBudgetRegionPlant.as_view(), name='cl_budget_region_plant'),
        path('budget/region-plant/<slug:region_name_slug>', views.ChooseYearBudgetRegionPlant.as_view(), name='cy_budget_region_plant'),
        path('budget/region-plant/<slug:region_name_slug>/<int:year>', views.BudgetRegionPlant.as_view(), name='budget_region_plant'),

        ### Budget by Region by Customer ###
        path('budget/region-customer/', views.ChooseLocationBudgetRegionCustomer.as_view(), name='cl_budget_region_customer'),
        path('budget/region-customer/<slug:region_name_slug>', views.ChooseYearBudgetRegionCustomer.as_view(), name='cy_budget_region_customer'),
        path('budget/region-customer/<slug:region_name_slug>/<int:year>', views.BudgetRegionCustomer.as_view(), name='budget_region_customer'),

        ### Budget by Region by Sector ###
        path('budget/region-sector/', views.ChooseLocationBudgetRegionSector.as_view(), name='cl_budget_region_sector'),
        path('budget/region-sector/<slug:region_name_slug>', views.ChooseYearBudgetRegionSector.as_view(), name='cy_budget_region_sector'),
        path('budget/region-sector/<slug:region_name_slug>/<int:year>', views.BudgetRegionSector.as_view(), name='budget_region_sector'),

        ### Global budget by Plant ###
        path('budget/global-plant/', views.ChooseYearBudgetGlobalPlant.as_view(), name='cy_budget_global_plant'),
        path('budget/global-plant/<int:year>', views.BudgetGlobalPlant.as_view(), name='budget_global_plant'),

        ### Global budget by Customer ###
        path('budget/global-customer/', views.ChooseYearBudgetGlobalCustomer.as_view(), name='cy_budget_global_customer'),
        path('budget/global-customer/<int:year>', views.BudgetGlobalCustomer.as_view(), name='budget_global_customer'),

        ### Global budget by Sector ###
        path('budget/global-sector/', views.ChooseYearBudgetGlobalSector.as_view(), name='cy_budget_global_sector'),
        path('budget/global-sector/<int:year>', views.BudgetGlobalSector.as_view(), name='budget_global_sector'),

        ### Global budget by Region ###
        path('budget/global-region/', views.ChooseYearBudgetGlobalRegion.as_view(), name='cy_budget_global_region'),
        path('budget/global-region/<int:year>', views.BudgetGlobalRegion.as_view(), name='budget_global_region'),

        ### Sales by Customer by Plant ###
        path('sale/customer-plant/', views.ChooseCustomerSaleCustomerPlant.as_view(), name='cc_sale_customer_plant'),
        path('sale/customer-plant/<slug:customer_name_slug>/', views.ChooseYearSaleCustomerPlant.as_view(), name='cy_sale_customer_plant'),
        path('sale/customer-plant/<slug:customer_name_slug>/<int:year>/', views.SaleCustomerPlant.as_view(), name='sale_customer_plant'),

        ### Sales by Plant by Customer ###
        path('sale/plant-customer/', views.ChooseLocationSalePlantCustomer.as_view(), name='cl_sale_plant_customer'),
        path('sale/plant-customer/<slug:location_name_slug>', views.ChooseYearSalePlantCustomer.as_view(), name='cy_sale_plant_customer'),
        path('sale/plant-customer/<slug:location_name_slug>/<int:year>', views.SalePlantCustomer.as_view(), name='sale_plant_customer'),

        ### Sales by Plant by Sector ###
        path('sale/plant-sector/', views.ChooseLocationSalePlantSector.as_view(), name='cl_sale_plant_sector'),
        path('sale/plant-sector/<slug:location_name_slug>', views.ChooseYearSalePlantSector.as_view(), name='cy_sale_plant_sector'),
        path('sale/plant-sector/<slug:location_name_slug>/<int:year>', views.SalePlantSector.as_view(), name='sale_plant_sector'),

        ### Sales by Region by Plant ###
        path('sale/region-plant/', views.ChooseLocationSaleRegionPlant.as_view(), name='cl_sale_region_plant'),
        path('sale/region-plant/<slug:region_name_slug>', views.ChooseYearSaleRegionPlant.as_view(), name='cy_sale_region_plant'),
        path('sale/region-plant/<slug:region_name_slug>/<int:year>', views.SaleRegionPlant.as_view(), name='sale_region_plant'),

        ### Sales by Region by Customer ###
        path('sale/region-customer/', views.ChooseLocationSaleRegionCustomer.as_view(), name='cl_sale_region_customer'),
        path('sale/region-customer/<slug:region_name_slug>', views.ChooseYearSaleRegionCustomer.as_view(), name='cy_sale_region_customer'),
        path('sale/region-customer/<slug:region_name_slug>/<int:year>', views.SaleRegionCustomer.as_view(), name='sale_region_customer'),

        ### Sales by Region by Sector ###
        path('sale/region-sector/', views.ChooseLocationSaleRegionSector.as_view(), name='cl_sale_region_sector'),
        path('sale/region-sector/<slug:region_name_slug>', views.ChooseYearSaleRegionSector.as_view(), name='cy_sale_region_sector'),
        path('sale/region-sector/<slug:region_name_slug>/<int:year>', views.SaleRegionSector.as_view(), name='sale_region_sector'),

        ### Global sales by Plant ###
        path('sale/global-plant/', views.ChooseYearSaleGlobalPlant.as_view(), name='cy_sale_global_plant'),
        path('sale/global-plant/<int:year>', views.SaleGlobalPlant.as_view(), name='sale_global_plant'),
        
        ### Global sales by Customer ###
        path('sale/global-customer/', views.ChooseYearSaleGlobalCustomer.as_view(), name='cy_sale_global_customer'),
        path('sale/global-customer/<int:year>', views.SaleGlobalCustomer.as_view(), name='sale_global_customer'),

        ### Global sales by Sector ###
        path('sale/global-sector/', views.ChooseYearSaleGlobalSector.as_view(), name='cy_sale_global_sector'),
        path('sale/global-sector/<int:year>', views.SaleGlobalSector.as_view(), name='sale_global_sector'),

        ### Global sales by Region ###
        path('sale/global-region/', views.ChooseYearSaleGlobalRegion.as_view(), name='cy_sale_global_region'),
        path('sale/global-region/<int:year>', views.SaleGlobalRegion.as_view(), name='sale_global_region'),

        ### VS Customer by Plant ###
        path('vs/customer-plant/', views.ChooseCustomerVsCustomerPlant.as_view(), name='cc_vs_customer_plant'),
        path('vs/customer-plant/<slug:customer_name_slug>/', views.ChooseYearVsCustomerPlant.as_view(), name='cy_vs_customer_plant'),
        path('vs/customer-plant/<slug:customer_name_slug>/<int:year>/', views.ChooseQuarterVsCustomerPlant.as_view(), name='cq_vs_customer_plant'),
        path('vs/customer-plant/<slug:customer_name_slug>/<int:year>/<str:q>/', views.VsCustomerPlant.as_view(), name='vs_customer_plant'),
         
        ### VS Plant by Customer ###
        path('vs/plant-customer/', views.ChooseLocationVsPlantCustomer.as_view(), name='cl_vs_plant_customer'),
        path('vs/plant-customer/<slug:location_name_slug>/', views.ChooseYearVsPlantCustomer.as_view(), name='cy_vs_plant_customer'),
        path('vs/plant-customer/<slug:location_name_slug>/<int:year>/', views.ChooseQuarterVsPlantCustomer.as_view(), name='cq_vs_plant_customer'),
        path('vs/plant-customer/<slug:location_name_slug>/<int:year>/<str:q>', views.VsPlantCustomer.as_view(), name='vs_plant_customer'),

        ### VS Plant by Sector ###
        path('vs/plant-sector/', views.ChooseLocationVsPlantSector.as_view(), name='cl_vs_plant_sector'),
        path('vs/plant-sector/<slug:location_name_slug>/', views.ChooseYearVsPlantSector.as_view(), name='cy_vs_plant_sector'),
        path('vs/plant-sector/<slug:location_name_slug>/<int:year>/', views.ChooseQuarterVsPlantSector.as_view(), name='cq_vs_plant_sector'),
        path('vs/plant-sector/<slug:location_name_slug>/<int:year>/<str:q>/', views.VsPlantSector.as_view(), name='vs_plant_sector'),

        ### VS Region by Plant ###
        path('vs/region-plant/', views.ChooseLocationVsRegionPlant.as_view(), name='cl_vs_region_plant'),
        path('vs/region-plant/<slug:region_name_slug>/', views.ChooseYearVsRegionPlant.as_view(), name='cy_vs_region_plant'),
        path('vs/region-plant/<slug:region_name_slug>/<int:year>/', views.ChooseQuarterVsRegionPlant.as_view(), name='cq_vs_region_plant'),
        path('vs/region-plant/<slug:region_name_slug>/<int:year>/<str:q>/', views.VsRegionPlant.as_view(), name='vs_region_plant'),

        ### VS Region by Customer ###
        path('vs/region-customer', views.ChooseLocationVsRegionCustomer.as_view(), name='cl_vs_region_customer'),
        path('vs/region-customer/<slug:region_name_slug>/', views.ChooseYearVsRegionCustomer.as_view(), name='cy_vs_region_customer'),
        path('vs/region-customer/<slug:region_name_slug>/<int:year>/', views.ChooseQuarterVsRegionCustomer.as_view(), name='cq_vs_region_customer'),
        path('vs/region-customer/<slug:region_name_slug>/<int:year>/<str:q>/', views.VsRegionCustomer.as_view(), name='vs_region_customer'),

        ### VS Region by Sector ###
        path('vs/region-sector/', views.ChooseLocationVsRegionSector.as_view(), name='cl_vs_region_sector'),
        path('vs/region-sector/<slug:region_name_slug>/', views.ChooseYearVsRegionSector.as_view(), name='cy_vs_region_sector'),
        path('vs/region-sector/<slug:region_name_slug>/<int:year>/', views.ChooseQuarterVsRegionSector.as_view(), name='cq_vs_region_sector'),
        path('vs/region-sector/<slug:region_name_slug>/<int:year>/<str:q>/', views.VsRegionSector.as_view(), name='vs_region_sector'),

        ### VS Global by Plant ###
        path('vs/global-plant/', views.ChooseYearVsGlobalPlant.as_view(), name='cy_vs_global_plant'),
        path('vs/global-plant/<int:year>/', views.ChooseQuarterVsGlobalPlant.as_view(), name='cq_vs_global_plant'),
        path('vs/global-plant/<int:year>/<str:q>/', views.VsGlobalPlant.as_view(), name='vs_global_plant'),

        ### VS Global by Customer ###
        path('vs/global-customer/', views.ChooseYearVsGlobalCustomer.as_view(), name='cy_vs_global_customer'),
        path('vs/global-customer/<int:year>/', views.ChooseQuarterVsGlobalCustomer.as_view(), name='cq_vs_global_customer'),
        path('vs/global-customer/<int:year>/<str:q>/', views.VsGlobalCustomer.as_view(), name='vs_global_customer'),

        ### VS Global by Sector ###
        path('vs/global-sector/', views.ChooseYearVsGlobalSector.as_view(), name='cy_vs_global_sector'),
        path('vs/global-sector/<int:year>/', views.ChooseQuarterVsGlobalSector.as_view(), name='cq_vs_global_sector'),
        path('vs/global-sector/<int:year>/<str:q>/', views.VsGlobalSector.as_view(), name='vs_global_sector'),

        ### VS Global by Region ###
        path('vs/global-region/', views.ChooseYearVsGlobalRegion.as_view(), name='cy_vs_global_region'),
        path('vs/global-region/<int:year>/', views.ChooseQuarterVsGlobalRegion.as_view(), name='cq_vs_global_region'),
        path('vs/global-region/<int:year>/<str:q>/', views.VsGlobalRegion.as_view(), name='vs_global_region'),
]
