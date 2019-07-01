from django.contrib import admin

from .models import Budget, Capability, Customer, Location, Region, Sale, Sector

class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('location', 'customer', 'year')
    exclude = ['q1', 'q2', 'q3', 'q4']

admin.site.register(Budget, BudgetAdmin)
admin.site.register(Capability)
admin.site.register(Customer)
admin.site.register(Location, LocationAdmin)
admin.site.register(Region)
admin.site.register(Sale)
admin.site.register(Sector)

admin.site.site_header = 'SalesQuery Administration'
admin.site.index_title = 'All models'
admin.site.site_title = 'SalesQuery Admin Portal'