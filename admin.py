from django.contrib import admin

from .models import Budget, Capability, Customer, Location, Region, Sale, Sector

class RegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class CustomerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('sector',)

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('location', 'customer', 'year')
    list_filter = ('year', 'customer__sector', 'location', 'customer')
    exclude = ['q1', 'q2', 'q3', 'q4']

class SaleAdmin(admin.ModelAdmin):
    list_display = ('location', 'customer', 'format_date')
    list_filter = ('location', 'customer',)
    exclude = ['q1', 'q2', 'q3', 'q4']

    @classmethod
    def format_date(self, obj):
        return obj.date.strftime('%b, %Y')

    format_date.admin_order_field = 'date'
    format_date.short_description = 'Date'

admin.site.register(Budget, BudgetAdmin)
admin.site.register(Capability)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Sector)

admin.site.site_header = 'Ledger Administration'
admin.site.index_title = 'All models'
admin.site.site_title = 'Ledger Admin Portal'