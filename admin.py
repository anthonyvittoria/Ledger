from django.contrib import admin

from .models import Budget, Capability, Customer, Location, Region, Sale, Sector

admin.site.register(Budget)
admin.site.register(Capability)
admin.site.register(Customer)
admin.site.register(Location)
admin.site.register(Region)
admin.site.register(Sale)
admin.site.register(Sector)
