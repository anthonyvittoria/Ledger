from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('sale/', views.choose_sale, name='choose_sale'),
        path('sale/<slug:location_name_slug>', views.index, name='index'),
        path('budget/', views.choose_budget, name='choose_budget'),
        path('budget/<slug:location_name_slug>', views.budget, name='budget'),
]
