from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('sale/', views.choose_sale, name='choose_sale'),
        path('sale/location/<slug:location_name_slug>', views.sale_by_location, name='sale_by_location'),
        path('sale/customer/<slug:customer_name_slug>', views.sale_by_customer, name='sale_by_customer'),
        path('budget/', views.choose_budget_location, name='choose_budget_location'),
        path('budget/<slug:location_name_slug>', views.choose_budget_year, name='choose_budget_year'),
        path('budget/<slug:location_name_slug>/<int:year>', views.budget, name='budget'),
]
