from django.contrib import admin

from .models import Budget, Capability, Customer, Location, Region, Sale, Sector

class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class CustomerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('location', 'customer', 'year')
    exclude = ['q1', 'q2', 'q3', 'q4']

class SaleAdmin(admin.ModelAdmin):
    list_display = ('location', 'customer', 'format_date')

    def format_date(self, obj):
        return obj.date.strftime('%b, %Y')

    format_date.admin_order_field = 'date'
    format_date.short_description = 'Date'

admin.site.register(Budget, BudgetAdmin)
admin.site.register(Capability)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Region)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Sector)

admin.site.site_header = 'SalesQuery Administration'
admin.site.index_title = 'All models'
admin.site.site_title = 'SalesQuery Admin Portal'