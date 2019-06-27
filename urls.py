from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('budget/', views.choose_budget, name='choose_budget'),
        path('budget/<int:id>', views.budget, name='budget'),
]
