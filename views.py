from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from .models import Budget, Customer, Sale, Location, Region
from .utilities import intersection

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'Ledger/index.html'

# Base Views
class ChooseCustomerView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'Ledger/choose_customer.html'

class ChooseLocationView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'Ledger/choose_location.html'

class ChooseYearView(LoginRequiredMixin, TemplateView):
    template_name = 'Ledger/choose_year.html'

class BudgetView(LoginRequiredMixin, TemplateView):
    template_name = 'Ledger/budget.html'

class SaleView(LoginRequiredMixin, TemplateView):
    template_name = 'Ledger/sale.html'

class ChooseQuarterView(LoginRequiredMixin, TemplateView):
    template_name = 'Ledger/choose_quarter.html'

class VersusView(LoginRequiredMixin, TemplateView):
    template_name = 'Ledger/versus.html'

#################################################
########## BUDGET BY CUSTOMER BY PLANT ##########
#################################################

class ChooseCustomerBudgetCustomerPlant(ChooseCustomerView):
    def get_context_data(self, **kwargs):
        customers = {budget.customer for budget in Budget.objects.all()}
        context = super().get_context_data(**kwargs)
        context['redirect'] = 'cy_budget_customer_plant'
        context['bc_first'] = 'Select Customer'
        context['object_list'] = customers
        return context

class ChooseYearBudgetCustomerPlant(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {budget.year for budget in Budget.objects.filter(
            customer__slug=self.kwargs['customer_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['test'] = self.kwargs
        context['redirect'] = 'budget_customer_plant'
        context['location_name_slug'] = self.kwargs['customer_name_slug']
        context['bc_second'] = Customer.objects.get(slug=self.kwargs['customer_name_slug'])
        context['years'] = years
        return context

class BudgetCustomerPlant(BudgetView):
    def get_context_data(self, **kwargs):
        budgets = Budget.objects.filter(
            customer__slug=self.kwargs['customer_name_slug'],
            year=self.kwargs['year']
        )
        data = {}
        for budget in budgets:
            if budget.location not in data.keys():
                data[budget.location] = {
                    'jan': budget.jan,
                    'feb': budget.feb,
                    'mar': budget.mar,
                    'apr': budget.apr,
                    'may': budget.may,
                    'jun': budget.jun,
                    'jul': budget.jul,
                    'aug': budget.aug,
                    'sep': budget.sep,
                    'oct': budget.oct,
                    'nov': budget.nov,
                    'dec': budget.dec,
                    'q1': budget.q1,
                    'q2': budget.q2,
                    'q3': budget.q3,
                    'q4': budget.q4,
                }
            else:
                data[budget.location]['jan'] += budget.jan
                data[budget.location]['feb'] += budget.feb
                data[budget.location]['mar'] += budget.mar
                data[budget.location]['apr'] += budget.apr
                data[budget.location]['may'] += budget.may
                data[budget.location]['jun'] += budget.jun
                data[budget.location]['jul'] += budget.jul
                data[budget.location]['aug'] += budget.aug
                data[budget.location]['sep'] += budget.sep
                data[budget.location]['oct'] += budget.oct
                data[budget.location]['nov'] += budget.nov
                data[budget.location]['dec'] += budget.dec
                data[budget.location]['q1'] += budget.q1
                data[budget.location]['q2'] += budget.q2
                data[budget.location]['q3'] += budget.q3
                data[budget.location]['q4'] += budget.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        budget_total = 0
        for plant in data:
            jan_total += data[plant]['jan']
            feb_total += data[plant]['feb']
            mar_total += data[plant]['mar']
            apr_total += data[plant]['apr']
            may_total += data[plant]['may']
            jun_total += data[plant]['jun']
            jul_total += data[plant]['jul']
            aug_total += data[plant]['aug']
            sep_total += data[plant]['sep']
            oct_total += data[plant]['oct']
            nov_total += data[plant]['nov']
            dec_total += data[plant]['dec']
            q1_total += data[plant]['q1']
            q2_total += data[plant]['q2']
            q3_total += data[plant]['q3']
            q4_total += data[plant]['q4']
            budget_total += (data[plant]['q1'] + data[plant]['q2'] + data[plant]['q3'] + data[plant]['q4'])
        context = super().get_context_data(**kwargs)
        context['budget_data'] = data
        context['first_col'] = 'plant'
        context['customer'] = Customer.objects.get(slug=self.kwargs['customer_name_slug'])
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['budget_total'] = budget_total
        return context

#################################################
########## BUDGET BY PLANT BY CUSTOMER ##########
#################################################

class ChooseLocationBudgetPlantCustomer(ChooseLocationView):
    def get_context_data(self, **kwargs):
        budget_locations = {budget.location for budget in Budget.objects.all().order_by('location__name')}
        context = super().get_context_data(**kwargs)
        context['redirect'] = 'cy_budget_plant_customer'
        context['locations'] = budget_locations
        return context

class ChooseYearBudgetPlantCustomer(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {budget.year for budget in Budget.objects.filter(
            location__slug=self.kwargs['location_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['redirect'] = 'budget_plant_customer'
        context['location_name_slug'] = self.kwargs['location_name_slug']
        context['years'] = years
        return context

class BudgetPlantCustomer(BudgetView):
    def get_context_data(self, **kwargs):
        budgets = Budget.objects.filter(
            location__slug=self.kwargs['location_name_slug'],
            year=self.kwargs['year']
        ).order_by('customer__name')

        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        budget_total = 0

        for budget in budgets:
            jan_total += budget.jan
            feb_total += budget.feb
            mar_total += budget.mar
            apr_total += budget.apr
            may_total += budget.may
            jun_total += budget.jun
            jul_total += budget.jul
            aug_total += budget.aug
            sep_total += budget.sep
            oct_total += budget.oct
            nov_total += budget.nov
            dec_total += budget.dec
            q1_total += budget.q1
            q2_total += budget.q2
            q3_total += budget.q3
            q4_total += budget.q4
            budget_total += (budget.q1 + budget.q2 + budget.q3 + budget.q4)

        context = super().get_context_data(**kwargs)
        context['budget_objects'] = budgets
        context['location'] = Location.objects.get(slug=self.kwargs['location_name_slug'])
        context['first_col'] = 'customer'
        context['second_col'] = 'sector'
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['budget_total'] = budget_total
        return context

###############################################
########## BUDGET BY PLANT BY SECTOR ##########
###############################################

class ChooseLocationBudgetPlantSector(ChooseLocationView):
    def get_context_data(self, **kwargs):
        budget_locations = {budget.location for budget in Budget.objects.all().order_by('location__name')}
        context = super().get_context_data(**kwargs)
        context['locations'] = budget_locations
        context['redirect'] = 'cy_budget_plant_sector'
        return context

class ChooseYearBudgetPlantSector(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {budget.year for budget in Budget.objects.filter(
            location__slug=self.kwargs['location_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['location_name_slug'] = self.kwargs['location_name_slug']
        context['redirect'] = 'budget_plant_sector'
        return context

class BudgetPlantSector(BudgetView):
    def get_context_data(self, **kwargs):
        budgets = Budget.objects.filter(
            location__slug=self.kwargs['location_name_slug'],
            year=self.kwargs['year']
        ).order_by('customer__sector')

        data = {}
        for budget in budgets:
            if budget.customer.sector not in data.keys():
                data[budget.customer.sector] = {
                    'jan': budget.jan,
                    'feb': budget.feb,
                    'mar': budget.mar,
                    'apr': budget.apr,
                    'may': budget.may,
                    'jun': budget.jun,
                    'jul': budget.jul,
                    'aug': budget.aug,
                    'sep': budget.sep,
                    'oct': budget.oct,
                    'nov': budget.nov,
                    'dec': budget.dec,
                    'q1': budget.q1,
                    'q2': budget.q2,
                    'q3': budget.q3,
                    'q4': budget.q4,
                }
            else:
                data[budget.customer.sector]['jan'] += budget.jan
                data[budget.customer.sector]['feb'] += budget.feb
                data[budget.customer.sector]['mar'] += budget.mar
                data[budget.customer.sector]['apr'] += budget.apr
                data[budget.customer.sector]['may'] += budget.may
                data[budget.customer.sector]['jun'] += budget.jun
                data[budget.customer.sector]['jul'] += budget.jul
                data[budget.customer.sector]['aug'] += budget.aug
                data[budget.customer.sector]['sep'] += budget.sep
                data[budget.customer.sector]['oct'] += budget.oct
                data[budget.customer.sector]['nov'] += budget.nov
                data[budget.customer.sector]['dec'] += budget.dec
                data[budget.customer.sector]['q1'] += budget.q1
                data[budget.customer.sector]['q2'] += budget.q2
                data[budget.customer.sector]['q3'] += budget.q3
                data[budget.customer.sector]['q4'] += budget.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        budget_total = 0
        for sector in data:
            jan_total += data[sector]['jan']
            feb_total += data[sector]['feb']
            mar_total += data[sector]['mar']
            apr_total += data[sector]['apr']
            may_total += data[sector]['may']
            jun_total += data[sector]['jun']
            jul_total += data[sector]['jul']
            aug_total += data[sector]['aug']
            sep_total += data[sector]['sep']
            oct_total += data[sector]['oct']
            nov_total += data[sector]['nov']
            dec_total += data[sector]['dec']
            q1_total += data[sector]['q1']
            q2_total += data[sector]['q2']
            q3_total += data[sector]['q3']
            q4_total += data[sector]['q4']
            budget_total += (data[sector]['q1'] + data[sector]['q2'] + data[sector]['q3'] + data[sector]['q4'])
        context = super().get_context_data(**kwargs)
        context['budget_data'] = data
        context['location'] = Location.objects.get(slug=self.kwargs['location_name_slug'])
        context['first_col'] = 'sector'
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['budget_total'] = budget_total
        return context

###############################################
########## BUDGET BY REGION BY PLANT ##########
###############################################

class ChooseLocationBudgetRegionPlant(ChooseLocationView):
    def get_context_data(self, **kwargs):
        regions = {budget.location.region for budget in Budget.objects.all().order_by('location__name')}
        context = super().get_context_data(**kwargs)
        context['locations'] = regions
        context['redirect'] = 'cy_budget_region_plant'
        return context

class ChooseYearBudgetRegionPlant(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {budget.year for budget in Budget.objects.filter(
            location__region__slug=self.kwargs['region_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['location_name_slug'] = self.kwargs['region_name_slug']
        context['redirect'] = 'budget_region_plant'
        return context

class BudgetRegionPlant(BudgetView):
    def get_context_data(self, **kwargs):
        budgets = Budget.objects.filter(
            location__region__slug=self.kwargs['region_name_slug'],
            year=self.kwargs['year']
        ).order_by('location__name')
        data = {}
        for budget in budgets:
            if budget.location not in data.keys():
                data[budget.location] = {
                    'jan': budget.jan,
                    'feb': budget.feb,
                    'mar': budget.mar,
                    'apr': budget.apr,
                    'may': budget.may,
                    'jun': budget.jun,
                    'jul': budget.jul,
                    'aug': budget.aug,
                    'sep': budget.sep,
                    'oct': budget.oct,
                    'nov': budget.nov,
                    'dec': budget.dec,
                    'q1': budget.q1,
                    'q2': budget.q2,
                    'q3': budget.q3,
                    'q4': budget.q4,
                }
            else:
                data[budget.location]['jan'] += budget.jan
                data[budget.location]['feb'] += budget.feb
                data[budget.location]['mar'] += budget.mar
                data[budget.location]['apr'] += budget.apr
                data[budget.location]['may'] += budget.may
                data[budget.location]['jun'] += budget.jun
                data[budget.location]['jul'] += budget.jul
                data[budget.location]['aug'] += budget.aug
                data[budget.location]['sep'] += budget.sep
                data[budget.location]['oct'] += budget.oct
                data[budget.location]['nov'] += budget.nov
                data[budget.location]['dec'] += budget.dec
                data[budget.location]['q1'] += budget.q1
                data[budget.location]['q2'] += budget.q2
                data[budget.location]['q3'] += budget.q3
                data[budget.location]['q4'] += budget.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        budget_total = 0
        for plant in data:
            jan_total += data[plant]['jan']
            feb_total += data[plant]['feb']
            mar_total += data[plant]['mar']
            apr_total += data[plant]['apr']
            may_total += data[plant]['may']
            jun_total += data[plant]['jun']
            jul_total += data[plant]['jul']
            aug_total += data[plant]['aug']
            sep_total += data[plant]['sep']
            oct_total += data[plant]['oct']
            nov_total += data[plant]['nov']
            dec_total += data[plant]['dec']
            q1_total += data[plant]['q1']
            q2_total += data[plant]['q2']
            q3_total += data[plant]['q3']
            q4_total += data[plant]['q4']
            budget_total += (data[plant]['q1'] + data[plant]['q2'] + data[plant]['q3'] + data[plant]['q4'])
        context = super().get_context_data(**kwargs)
        context['budget_data'] = data
        context['first_col'] = 'plant'
        context['region'] = budgets[0].location.region
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['budget_total'] = budget_total
        return context

##################################################
########## BUDGET BY REGION BY CUSTOMER ##########
##################################################

class ChooseLocationBudgetRegionCustomer(ChooseLocationView):
    def get_context_data(self, **kwargs):
        regions = {budget.location.region for budget in Budget.objects.all().order_by('location__name')}
        context = super().get_context_data(**kwargs)
        context['locations'] = regions
        context['redirect'] = 'cy_budget_region_customer'
        return context

class ChooseYearBudgetRegionCustomer(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {budget.year for budget in Budget.objects.filter(
            location__region__slug=self.kwargs['region_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['location_name_slug'] = self.kwargs['region_name_slug']
        context['redirect'] = 'budget_region_customer'
        return context

class BudgetRegionCustomer(BudgetView):
    def get_context_data(self, **kwargs):
        budgets = Budget.objects.filter(
            location__region__slug=self.kwargs['region_name_slug'],
            year=self.kwargs['year']
        ).order_by('customer__name')
        data = {}
        for budget in budgets:
            if budget.customer not in data.keys():
                data[budget.customer] = {
                    'jan': budget.jan,
                    'feb': budget.feb,
                    'mar': budget.mar,
                    'apr': budget.apr,
                    'may': budget.may,
                    'jun': budget.jun,
                    'jul': budget.jul,
                    'aug': budget.aug,
                    'sep': budget.sep,
                    'oct': budget.oct,
                    'nov': budget.nov,
                    'dec': budget.dec,
                    'q1': budget.q1,
                    'q2': budget.q2,
                    'q3': budget.q3,
                    'q4': budget.q4,
                }
            else:
                data[budget.customer]['jan'] += budget.jan
                data[budget.customer]['feb'] += budget.feb
                data[budget.customer]['mar'] += budget.mar
                data[budget.customer]['apr'] += budget.apr
                data[budget.customer]['may'] += budget.may
                data[budget.customer]['jun'] += budget.jun
                data[budget.customer]['jul'] += budget.jul
                data[budget.customer]['aug'] += budget.aug
                data[budget.customer]['sep'] += budget.sep
                data[budget.customer]['oct'] += budget.oct
                data[budget.customer]['nov'] += budget.nov
                data[budget.customer]['dec'] += budget.dec
                data[budget.customer]['q1'] += budget.q1
                data[budget.customer]['q2'] += budget.q2
                data[budget.customer]['q3'] += budget.q3
                data[budget.customer]['q4'] += budget.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        budget_total = 0
        for customer in data:
            jan_total += data[customer]['jan']
            feb_total += data[customer]['feb']
            mar_total += data[customer]['mar']
            apr_total += data[customer]['apr']
            may_total += data[customer]['may']
            jun_total += data[customer]['jun']
            jul_total += data[customer]['jul']
            aug_total += data[customer]['aug']
            sep_total += data[customer]['sep']
            oct_total += data[customer]['oct']
            nov_total += data[customer]['nov']
            dec_total += data[customer]['dec']
            q1_total += data[customer]['q1']
            q2_total += data[customer]['q2']
            q3_total += data[customer]['q3']
            q4_total += data[customer]['q4']
            budget_total += (data[customer]['q1'] + data[customer]['q2'] + data[customer]['q3'] + data[customer]['q4'])
        context = super().get_context_data(**kwargs)
        context['budget_data'] = data
        context['first_col'] = 'customer'
        context['region'] = budgets[0].location.region
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['budget_total'] = budget_total
        return context

################################################
########## BUDGET BY REGION BY SECTOR ##########
################################################

class ChooseLocationBudgetRegionSector(ChooseLocationView):
    def get_context_data(self, **kwargs):
        regions = {budget.location.region for budget in Budget.objects.all().order_by('location__name')}
        context = super().get_context_data(**kwargs)
        context['locations'] = regions
        context['redirect'] = 'cy_budget_region_sector'
        return context

class ChooseYearBudgetRegionSector(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {budget.year for budget in Budget.objects.filter(
            location__region__slug=self.kwargs['region_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['location_name_slug'] = self.kwargs['region_name_slug']
        context['redirect'] = 'budget_region_sector'
        return context

class BudgetRegionSector(BudgetView):
    def get_context_data(self, **kwargs):
        budgets = Budget.objects.filter(
            location__region__slug=self.kwargs['region_name_slug'],
            year=self.kwargs['year']
        ).order_by('customer__sector')
        data = {}
        for budget in budgets:
            if budget.customer.sector not in data.keys():
                data[budget.customer.sector] = {
                    'jan': budget.jan,
                    'feb': budget.feb,
                    'mar': budget.mar,
                    'apr': budget.apr,
                    'may': budget.may,
                    'jun': budget.jun,
                    'jul': budget.jul,
                    'aug': budget.aug,
                    'sep': budget.sep,
                    'oct': budget.oct,
                    'nov': budget.nov,
                    'dec': budget.dec,
                    'q1': budget.q1,
                    'q2': budget.q2,
                    'q3': budget.q3,
                    'q4': budget.q4,
                }
            else:
                data[budget.customer.sector]['jan'] += budget.jan
                data[budget.customer.sector]['feb'] += budget.feb
                data[budget.customer.sector]['mar'] += budget.mar
                data[budget.customer.sector]['apr'] += budget.apr
                data[budget.customer.sector]['may'] += budget.may
                data[budget.customer.sector]['jun'] += budget.jun
                data[budget.customer.sector]['jul'] += budget.jul
                data[budget.customer.sector]['aug'] += budget.aug
                data[budget.customer.sector]['sep'] += budget.sep
                data[budget.customer.sector]['oct'] += budget.oct
                data[budget.customer.sector]['nov'] += budget.nov
                data[budget.customer.sector]['dec'] += budget.dec
                data[budget.customer.sector]['q1'] += budget.q1
                data[budget.customer.sector]['q2'] += budget.q2
                data[budget.customer.sector]['q3'] += budget.q3
                data[budget.customer.sector]['q4'] += budget.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        budget_total = 0
        for sector in data:
            jan_total += data[sector]['jan']
            feb_total += data[sector]['feb']
            mar_total += data[sector]['mar']
            apr_total += data[sector]['apr']
            may_total += data[sector]['may']
            jun_total += data[sector]['jun']
            jul_total += data[sector]['jul']
            aug_total += data[sector]['aug']
            sep_total += data[sector]['sep']
            oct_total += data[sector]['oct']
            nov_total += data[sector]['nov']
            dec_total += data[sector]['dec']
            q1_total += data[sector]['q1']
            q2_total += data[sector]['q2']
            q3_total += data[sector]['q3']
            q4_total += data[sector]['q4']
            budget_total += (data[sector]['q1'] + data[sector]['q2'] + data[sector]['q3'] + data[sector]['q4'])
        context = super().get_context_data(**kwargs)
        context['budget_data'] = data
        context['first_col'] = 'sector'
        context['region'] = budgets[0].location.region
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['budget_total'] = budget_total
        return context

###########################################
########## GLOBAL BUDGET BY PLANT ##########
###########################################

class ChooseYearBudgetGlobalPlant(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {budget.year for budget in Budget.objects.all().order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'budget_global_plant'
        return context

class BudgetGlobalPlant(BudgetView):
    def get_context_data(self, **kwargs):
        budgets = Budget.objects.filter(
            year=self.kwargs['year']
        ).order_by('location__name')
        data = {}
        for budget in budgets:
            if budget.location not in data.keys():
                data[budget.location] = {
                    'jan': budget.jan,
                    'feb': budget.feb,
                    'mar': budget.mar,
                    'apr': budget.apr,
                    'may': budget.may,
                    'jun': budget.jun,
                    'jul': budget.jul,
                    'aug': budget.aug,
                    'sep': budget.sep,
                    'oct': budget.oct,
                    'nov': budget.nov,
                    'dec': budget.dec,
                    'q1': budget.q1,
                    'q2': budget.q2,
                    'q3': budget.q3,
                    'q4': budget.q4,
                }
            else:
                data[budget.location]['jan'] += budget.jan
                data[budget.location]['feb'] += budget.feb
                data[budget.location]['mar'] += budget.mar
                data[budget.location]['apr'] += budget.apr
                data[budget.location]['may'] += budget.may
                data[budget.location]['jun'] += budget.jun
                data[budget.location]['jul'] += budget.jul
                data[budget.location]['aug'] += budget.aug
                data[budget.location]['sep'] += budget.sep
                data[budget.location]['oct'] += budget.oct
                data[budget.location]['nov'] += budget.nov
                data[budget.location]['dec'] += budget.dec
                data[budget.location]['q1'] += budget.q1
                data[budget.location]['q2'] += budget.q2
                data[budget.location]['q3'] += budget.q3
                data[budget.location]['q4'] += budget.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        budget_total = 0
        for plant in data:
            jan_total += data[plant]['jan']
            feb_total += data[plant]['feb']
            mar_total += data[plant]['mar']
            apr_total += data[plant]['apr']
            may_total += data[plant]['may']
            jun_total += data[plant]['jun']
            jul_total += data[plant]['jul']
            aug_total += data[plant]['aug']
            sep_total += data[plant]['sep']
            oct_total += data[plant]['oct']
            nov_total += data[plant]['nov']
            dec_total += data[plant]['dec']
            q1_total += data[plant]['q1']
            q2_total += data[plant]['q2']
            q3_total += data[plant]['q3']
            q4_total += data[plant]['q4']
            budget_total += (data[plant]['q1'] + data[plant]['q2'] + data[plant]['q3'] + data[plant]['q4'])
        context = super().get_context_data(**kwargs)
        context['budget_data'] = data
        context['global'] = True
        context['first_col'] = 'plant'
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['budget_total'] = budget_total
        return context

##############################################
########## GLOBAL BUDGET BY CUSTOMER ##########
##############################################

class ChooseYearBudgetGlobalCustomer(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {budget.year for budget in Budget.objects.all().order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'budget_global_customer'
        return context

class BudgetGlobalCustomer(BudgetView):
    def get_context_data(self, **kwargs):
        budgets = Budget.objects.filter(
            year=self.kwargs['year']
        ).order_by('customer__name')
        data = {}
        for budget in budgets:
            if budget.customer not in data.keys():
                data[budget.customer] = {
                    'jan': budget.jan,
                    'feb': budget.feb,
                    'mar': budget.mar,
                    'apr': budget.apr,
                    'may': budget.may,
                    'jun': budget.jun,
                    'jul': budget.jul,
                    'aug': budget.aug,
                    'sep': budget.sep,
                    'oct': budget.oct,
                    'nov': budget.nov,
                    'dec': budget.dec,
                    'q1': budget.q1,
                    'q2': budget.q2,
                    'q3': budget.q3,
                    'q4': budget.q4,
                }
            else:
                data[budget.customer]['jan'] += budget.jan
                data[budget.customer]['feb'] += budget.feb
                data[budget.customer]['mar'] += budget.mar
                data[budget.customer]['apr'] += budget.apr
                data[budget.customer]['may'] += budget.may
                data[budget.customer]['jun'] += budget.jun
                data[budget.customer]['jul'] += budget.jul
                data[budget.customer]['aug'] += budget.aug
                data[budget.customer]['sep'] += budget.sep
                data[budget.customer]['oct'] += budget.oct
                data[budget.customer]['nov'] += budget.nov
                data[budget.customer]['dec'] += budget.dec
                data[budget.customer]['q1'] += budget.q1
                data[budget.customer]['q2'] += budget.q2
                data[budget.customer]['q3'] += budget.q3
                data[budget.customer]['q4'] += budget.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        budget_total = 0
        for customer in data:
            jan_total += data[customer]['jan']
            feb_total += data[customer]['feb']
            mar_total += data[customer]['mar']
            apr_total += data[customer]['apr']
            may_total += data[customer]['may']
            jun_total += data[customer]['jun']
            jul_total += data[customer]['jul']
            aug_total += data[customer]['aug']
            sep_total += data[customer]['sep']
            oct_total += data[customer]['oct']
            nov_total += data[customer]['nov']
            dec_total += data[customer]['dec']
            q1_total += data[customer]['q1']
            q2_total += data[customer]['q2']
            q3_total += data[customer]['q3']
            q4_total += data[customer]['q4']
            budget_total += (data[customer]['q1'] + data[customer]['q2'] + data[customer]['q3'] + data[customer]['q4'])
        context = super().get_context_data(**kwargs)
        context['budget_data'] = data
        context['global'] = True
        context['first_col'] = 'customer'
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['budget_total'] = budget_total
        return context

############################################
########## GLOBAL BUDGET BY SECTOR ##########
############################################

class ChooseYearBudgetGlobalSector(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {budget.year for budget in Budget.objects.all().order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'budget_global_sector'
        return context

class BudgetGlobalSector(BudgetView):
    def get_context_data(self, **kwargs):
        budgets = Budget.objects.filter(
            year=self.kwargs['year']
        ).order_by('customer__sector')
        data = {}
        for budget in budgets:
            if budget.customer.sector not in data.keys():
                data[budget.customer.sector] = {
                    'jan': budget.jan,
                    'feb': budget.feb,
                    'mar': budget.mar,
                    'apr': budget.apr,
                    'may': budget.may,
                    'jun': budget.jun,
                    'jul': budget.jul,
                    'aug': budget.aug,
                    'sep': budget.sep,
                    'oct': budget.oct,
                    'nov': budget.nov,
                    'dec': budget.dec,
                    'q1': budget.q1,
                    'q2': budget.q2,
                    'q3': budget.q3,
                    'q4': budget.q4,
                }
            else:
                data[budget.customer.sector]['jan'] += budget.jan
                data[budget.customer.sector]['feb'] += budget.feb
                data[budget.customer.sector]['mar'] += budget.mar
                data[budget.customer.sector]['apr'] += budget.apr
                data[budget.customer.sector]['may'] += budget.may
                data[budget.customer.sector]['jun'] += budget.jun
                data[budget.customer.sector]['jul'] += budget.jul
                data[budget.customer.sector]['aug'] += budget.aug
                data[budget.customer.sector]['sep'] += budget.sep
                data[budget.customer.sector]['oct'] += budget.oct
                data[budget.customer.sector]['nov'] += budget.nov
                data[budget.customer.sector]['dec'] += budget.dec
                data[budget.customer.sector]['q1'] += budget.q1
                data[budget.customer.sector]['q2'] += budget.q2
                data[budget.customer.sector]['q3'] += budget.q3
                data[budget.customer.sector]['q4'] += budget.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        budget_total = 0
        for sector in data:
            jan_total += data[sector]['jan']
            feb_total += data[sector]['feb']
            mar_total += data[sector]['mar']
            apr_total += data[sector]['apr']
            may_total += data[sector]['may']
            jun_total += data[sector]['jun']
            jul_total += data[sector]['jul']
            aug_total += data[sector]['aug']
            sep_total += data[sector]['sep']
            oct_total += data[sector]['oct']
            nov_total += data[sector]['nov']
            dec_total += data[sector]['dec']
            q1_total += data[sector]['q1']
            q2_total += data[sector]['q2']
            q3_total += data[sector]['q3']
            q4_total += data[sector]['q4']
            budget_total += (data[sector]['q1'] + data[sector]['q2'] + data[sector]['q3'] + data[sector]['q4'])
        context = super().get_context_data(**kwargs)
        context['budget_data'] = data
        context['global'] = True
        context['first_col'] = 'sector'
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['budget_total'] = budget_total
        return context

############################################
########## GLOBAL BUDGET BY REGION ##########
############################################

class ChooseYearBudgetGlobalRegion(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {budget.year for budget in Budget.objects.all().order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'budget_global_region'
        return context

class BudgetGlobalRegion(BudgetView):
    def get_context_data(self, **kwargs):
        budgets = Budget.objects.filter(
            year=self.kwargs['year']
        ).order_by('location__region')
        data = {}
        for budget in budgets:
            if budget.location.region not in data.keys():
                data[budget.location.region] = {
                    'jan': budget.jan,
                    'feb': budget.feb,
                    'mar': budget.mar,
                    'apr': budget.apr,
                    'may': budget.may,
                    'jun': budget.jun,
                    'jul': budget.jul,
                    'aug': budget.aug,
                    'sep': budget.sep,
                    'oct': budget.oct,
                    'nov': budget.nov,
                    'dec': budget.dec,
                    'q1': budget.q1,
                    'q2': budget.q2,
                    'q3': budget.q3,
                    'q4': budget.q4,
                }
            else:
                data[budget.location.region]['jan'] += budget.jan
                data[budget.location.region]['feb'] += budget.feb
                data[budget.location.region]['mar'] += budget.mar
                data[budget.location.region]['apr'] += budget.apr
                data[budget.location.region]['may'] += budget.may
                data[budget.location.region]['jun'] += budget.jun
                data[budget.location.region]['jul'] += budget.jul
                data[budget.location.region]['aug'] += budget.aug
                data[budget.location.region]['sep'] += budget.sep
                data[budget.location.region]['oct'] += budget.oct
                data[budget.location.region]['nov'] += budget.nov
                data[budget.location.region]['dec'] += budget.dec
                data[budget.location.region]['q1'] += budget.q1
                data[budget.location.region]['q2'] += budget.q2
                data[budget.location.region]['q3'] += budget.q3
                data[budget.location.region]['q4'] += budget.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        budget_total = 0
        for region in data:
            jan_total += data[region]['jan']
            feb_total += data[region]['feb']
            mar_total += data[region]['mar']
            apr_total += data[region]['apr']
            may_total += data[region]['may']
            jun_total += data[region]['jun']
            jul_total += data[region]['jul']
            aug_total += data[region]['aug']
            sep_total += data[region]['sep']
            oct_total += data[region]['oct']
            nov_total += data[region]['nov']
            dec_total += data[region]['dec']
            q1_total += data[region]['q1']
            q2_total += data[region]['q2']
            q3_total += data[region]['q3']
            q4_total += data[region]['q4']
            budget_total += (data[region]['q1'] + data[region]['q2'] + data[region]['q3'] + data[region]['q4'])
        context = super().get_context_data(**kwargs)
        context['budget_data'] = data
        context['global'] = True
        context['first_col'] = 'region'
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['budget_total'] = budget_total
        return context

#################################################
########## ACTUALS BY CUSTOMER BY PLANT ##########
#################################################

class ChooseCustomerSaleCustomerPlant(ChooseCustomerView):
    def get_context_data(self, **kwargs):
        customers = {sale.customer for sale in Sale.objects.all()}
        context = super().get_context_data(**kwargs)
        context['redirect'] = 'cy_sale_customer_plant'
        context['object_list'] = customers
        return context

class ChooseYearSaleCustomerPlant(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {sale.year for sale in Sale.objects.filter(
            customer__slug=self.kwargs['customer_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['location_name_slug'] = self.kwargs['customer_name_slug']
        context['redirect'] = 'sale_customer_plant'
        return context

class SaleCustomerPlant(SaleView):
    def get_context_data(self, **kwargs):
        sales = Sale.objects.filter(
            customer__slug=self.kwargs['customer_name_slug'],
            year=self.kwargs['year']
        )
        data = {}
        for sale in sales:
            if sale.location not in data.keys():
                data[sale.location] = {
                    'jan': sale.jan,
                    'feb': sale.feb,
                    'mar': sale.mar,
                    'apr': sale.apr,
                    'may': sale.may,
                    'jun': sale.jun,
                    'jul': sale.jul,
                    'aug': sale.aug,
                    'sep': sale.sep,
                    'oct': sale.oct,
                    'nov': sale.nov,
                    'dec': sale.dec,
                    'q1': sale.q1,
                    'q2': sale.q2,
                    'q3': sale.q3,
                    'q4': sale.q4,
                }
            else:
                data[sale.location]['jan'] += sale.jan
                data[sale.location]['feb'] += sale.feb
                data[sale.location]['mar'] += sale.mar
                data[sale.location]['apr'] += sale.apr
                data[sale.location]['may'] += sale.may
                data[sale.location]['jun'] += sale.jun
                data[sale.location]['jul'] += sale.jul
                data[sale.location]['aug'] += sale.aug
                data[sale.location]['sep'] += sale.sep
                data[sale.location]['oct'] += sale.oct
                data[sale.location]['nov'] += sale.nov
                data[sale.location]['dec'] += sale.dec
                data[sale.location]['q1'] += sale.q1
                data[sale.location]['q2'] += sale.q2
                data[sale.location]['q3'] += sale.q3
                data[sale.location]['q4'] += sale.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        sale_total = 0
        for plant in data:
            jan_total += data[plant]['jan']
            feb_total += data[plant]['feb']
            mar_total += data[plant]['mar']
            apr_total += data[plant]['apr']
            may_total += data[plant]['may']
            jun_total += data[plant]['jun']
            jul_total += data[plant]['jul']
            aug_total += data[plant]['aug']
            sep_total += data[plant]['sep']
            oct_total += data[plant]['oct']
            nov_total += data[plant]['nov']
            dec_total += data[plant]['dec']
            q1_total += data[plant]['q1']
            q2_total += data[plant]['q2']
            q3_total += data[plant]['q3']
            q4_total += data[plant]['q4']
            sale_total += (data[plant]['q1'] + data[plant]['q2'] + data[plant]['q3'] + data[plant]['q4'])
        context = super().get_context_data(**kwargs)
        context['sale_data'] = data
        context['first_col'] = 'plant'
        context['customer'] = Customer.objects.get(slug=self.kwargs['customer_name_slug'])
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['sale_total'] = sale_total
        return context

##################################################
########## ACTUALS BY PLANT BY CUSTOMER ##########
##################################################

class ChooseLocationSalePlantCustomer(ChooseLocationView):
    def get_context_data(self, **kwargs):
        locations = {sale.location for sale in Sale.objects.all().order_by('location__name')}
        context = super().get_context_data(**kwargs)
        context['locations'] = locations
        context['redirect'] = 'cy_sale_plant_customer'
        return context

class ChooseYearSalePlantCustomer(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {sale.year for sale in Sale.objects.filter(
            location__slug=self.kwargs['location_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['location_name_slug'] = self.kwargs['location_name_slug']
        context['redirect'] = 'sale_plant_customer'
        return context

class SalePlantCustomer(SaleView):
    def get_context_data(self, **kwargs):
        sales = Sale.objects.filter(
            location__slug=self.kwargs['location_name_slug'],
            year=self.kwargs['year']
        ).order_by('customer__name')

        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        sale_total = 0

        for sale in sales:
            jan_total += sale.jan
            feb_total += sale.feb
            mar_total += sale.mar
            apr_total += sale.apr
            may_total += sale.may
            jun_total += sale.jun
            jul_total += sale.jul
            aug_total += sale.aug
            sep_total += sale.sep
            oct_total += sale.oct
            nov_total += sale.nov
            dec_total += sale.dec
            q1_total += sale.q1
            q2_total += sale.q2
            q3_total += sale.q3
            q4_total += sale.q4
            sale_total += (sale.q1 + sale.q2 + sale.q3 + sale.q4)

        context = super().get_context_data(**kwargs)
        context['sale_objects'] = sales
        context['location'] = Location.objects.get(slug=self.kwargs['location_name_slug'])
        context['first_col'] = 'customer'
        context['second_col'] = 'sector'
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['sale_total'] = sale_total
        return context

################################################
########## ACTUALS BY PLANT BY SECTOR ##########
################################################

class ChooseLocationSalePlantSector(ChooseLocationView):
    def get_context_data(self, **kwargs):
        locations = {sale.location for sale in Sale.objects.all().order_by('location__name')}
        context = super().get_context_data(**kwargs)
        context['locations'] = locations
        context['redirect'] = 'cy_sale_plant_sector'
        return context

class ChooseYearSalePlantSector(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {sale.year for sale in Sale.objects.filter(
            location__slug=self.kwargs['location_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['location_name_slug'] = self.kwargs['location_name_slug']
        context['redirect'] = 'sale_plant_sector'
        return context

class SalePlantSector(SaleView):
    def get_context_data(self, **kwargs):
        sales = Sale.objects.filter(
            location__slug=self.kwargs['location_name_slug'],
            year=self.kwargs['year']
        ).order_by('customer__sector')

        data = {}
        for sale in sales:
            if sale.customer.sector not in data.keys():
                data[sale.customer.sector] = {
                    'jan': sale.jan,
                    'feb': sale.feb,
                    'mar': sale.mar,
                    'apr': sale.apr,
                    'may': sale.may,
                    'jun': sale.jun,
                    'jul': sale.jul,
                    'aug': sale.aug,
                    'sep': sale.sep,
                    'oct': sale.oct,
                    'nov': sale.nov,
                    'dec': sale.dec,
                    'q1': sale.q1,
                    'q2': sale.q2,
                    'q3': sale.q3,
                    'q4': sale.q4,
                }
            else:
                data[sale.customer.sector]['jan'] += sale.jan
                data[sale.customer.sector]['feb'] += sale.feb
                data[sale.customer.sector]['mar'] += sale.mar
                data[sale.customer.sector]['apr'] += sale.apr
                data[sale.customer.sector]['may'] += sale.may
                data[sale.customer.sector]['jun'] += sale.jun
                data[sale.customer.sector]['jul'] += sale.jul
                data[sale.customer.sector]['aug'] += sale.aug
                data[sale.customer.sector]['sep'] += sale.sep
                data[sale.customer.sector]['oct'] += sale.oct
                data[sale.customer.sector]['nov'] += sale.nov
                data[sale.customer.sector]['dec'] += sale.dec
                data[sale.customer.sector]['q1'] += sale.q1
                data[sale.customer.sector]['q2'] += sale.q2
                data[sale.customer.sector]['q3'] += sale.q3
                data[sale.customer.sector]['q4'] += sale.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        sale_total = 0
        for sector in data:
            jan_total += data[sector]['jan']
            feb_total += data[sector]['feb']
            mar_total += data[sector]['mar']
            apr_total += data[sector]['apr']
            may_total += data[sector]['may']
            jun_total += data[sector]['jun']
            jul_total += data[sector]['jul']
            aug_total += data[sector]['aug']
            sep_total += data[sector]['sep']
            oct_total += data[sector]['oct']
            nov_total += data[sector]['nov']
            dec_total += data[sector]['dec']
            q1_total += data[sector]['q1']
            q2_total += data[sector]['q2']
            q3_total += data[sector]['q3']
            q4_total += data[sector]['q4']
            sale_total += (data[sector]['q1'] + data[sector]['q2'] + data[sector]['q3'] + data[sector]['q4'])
        context = super().get_context_data(**kwargs)
        context['sale_data'] = data
        context['location'] = Location.objects.get(slug=self.kwargs['location_name_slug'])
        context['first_col'] = 'sector'
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['sale_total'] = sale_total
        return context

################################################
########## ACTUALS BY REGION BY PLANT ##########
################################################

class ChooseLocationSaleRegionPlant(ChooseLocationView):
    def get_context_data(self, **kwargs):
        regions = {sale.location.region for sale in Sale.objects.all().order_by('location__name')}
        context = super().get_context_data(**kwargs)
        context['locations'] = regions
        context['redirect'] = 'cy_sale_region_plant'
        return context

class ChooseYearSaleRegionPlant(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {sale.year for sale in Sale.objects.filter(
            location__region__slug=self.kwargs['region_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['location_name_slug'] = self.kwargs['region_name_slug']
        context['redirect'] = 'sale_region_plant'
        return context

class SaleRegionPlant(SaleView):
    def get_context_data(self, **kwargs):
        sales = Sale.objects.filter(
            location__region__slug=self.kwargs['region_name_slug'],
            year=self.kwargs['year']
        ).order_by('location__name')
        data = {}
        for sale in sales:
            if sale.location not in data.keys():
                data[sale.location] = {
                    'jan': sale.jan,
                    'feb': sale.feb,
                    'mar': sale.mar,
                    'apr': sale.apr,
                    'may': sale.may,
                    'jun': sale.jun,
                    'jul': sale.jul,
                    'aug': sale.aug,
                    'sep': sale.sep,
                    'oct': sale.oct,
                    'nov': sale.nov,
                    'dec': sale.dec,
                    'q1': sale.q1,
                    'q2': sale.q2,
                    'q3': sale.q3,
                    'q4': sale.q4,
                }
            else:
                data[sale.location]['jan'] += sale.jan
                data[sale.location]['feb'] += sale.feb
                data[sale.location]['mar'] += sale.mar
                data[sale.location]['apr'] += sale.apr
                data[sale.location]['may'] += sale.may
                data[sale.location]['jun'] += sale.jun
                data[sale.location]['jul'] += sale.jul
                data[sale.location]['aug'] += sale.aug
                data[sale.location]['sep'] += sale.sep
                data[sale.location]['oct'] += sale.oct
                data[sale.location]['nov'] += sale.nov
                data[sale.location]['dec'] += sale.dec
                data[sale.location]['q1'] += sale.q1
                data[sale.location]['q2'] += sale.q2
                data[sale.location]['q3'] += sale.q3
                data[sale.location]['q4'] += sale.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        sale_total = 0
        for plant in data:
            jan_total += data[plant]['jan']
            feb_total += data[plant]['feb']
            mar_total += data[plant]['mar']
            apr_total += data[plant]['apr']
            may_total += data[plant]['may']
            jun_total += data[plant]['jun']
            jul_total += data[plant]['jul']
            aug_total += data[plant]['aug']
            sep_total += data[plant]['sep']
            oct_total += data[plant]['oct']
            nov_total += data[plant]['nov']
            dec_total += data[plant]['dec']
            q1_total += data[plant]['q1']
            q2_total += data[plant]['q2']
            q3_total += data[plant]['q3']
            q4_total += data[plant]['q4']
            sale_total += (data[plant]['q1'] + data[plant]['q2'] + data[plant]['q3'] + data[plant]['q4'])
        context = super().get_context_data(**kwargs)
        context['sale_data'] = data
        context['first_col'] = 'plant'
        context['region'] = sales[0].location.region
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['sale_total'] = sale_total
        return context

###################################################
########## ACTUALS BY REGION BY CUSTOMER ##########
###################################################

class ChooseLocationSaleRegionCustomer(ChooseLocationView):
    def get_context_data(self, **kwargs):
        regions = {sale.location.region for sale in Sale.objects.all().order_by('location__name')}
        context = super().get_context_data(**kwargs)
        context['locations'] = regions
        context['redirect'] = 'cy_sale_region_customer'
        return context

class ChooseYearSaleRegionCustomer(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {sale.year for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['location_name_slug'] = self.kwargs['region_name_slug']
        context['redirect'] = 'sale_region_customer'
        return context

class SaleRegionCustomer(SaleView):
    def get_context_data(self, **kwargs):
        sales = Sale.objects.filter(
            location__region__slug=self.kwargs['region_name_slug'],
            year=self.kwargs['year']
        ).order_by('customer__name')
        data = {}
        for sale in sales:
            if sale.customer not in data.keys():
                data[sale.customer] = {
                    'jan': sale.jan,
                    'feb': sale.feb,
                    'mar': sale.mar,
                    'apr': sale.apr,
                    'may': sale.may,
                    'jun': sale.jun,
                    'jul': sale.jul,
                    'aug': sale.aug,
                    'sep': sale.sep,
                    'oct': sale.oct,
                    'nov': sale.nov,
                    'dec': sale.dec,
                    'q1': sale.q1,
                    'q2': sale.q2,
                    'q3': sale.q3,
                    'q4': sale.q4,
                }
            else:
                data[sale.customer]['jan'] += sale.jan
                data[sale.customer]['feb'] += sale.feb
                data[sale.customer]['mar'] += sale.mar
                data[sale.customer]['apr'] += sale.apr
                data[sale.customer]['may'] += sale.may
                data[sale.customer]['jun'] += sale.jun
                data[sale.customer]['jul'] += sale.jul
                data[sale.customer]['aug'] += sale.aug
                data[sale.customer]['sep'] += sale.sep
                data[sale.customer]['oct'] += sale.oct
                data[sale.customer]['nov'] += sale.nov
                data[sale.customer]['dec'] += sale.dec
                data[sale.customer]['q1'] += sale.q1
                data[sale.customer]['q2'] += sale.q2
                data[sale.customer]['q3'] += sale.q3
                data[sale.customer]['q4'] += sale.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        sale_total = 0
        for customer in data:
            jan_total += data[customer]['jan']
            feb_total += data[customer]['feb']
            mar_total += data[customer]['mar']
            apr_total += data[customer]['apr']
            may_total += data[customer]['may']
            jun_total += data[customer]['jun']
            jul_total += data[customer]['jul']
            aug_total += data[customer]['aug']
            sep_total += data[customer]['sep']
            oct_total += data[customer]['oct']
            nov_total += data[customer]['nov']
            dec_total += data[customer]['dec']
            q1_total += data[customer]['q1']
            q2_total += data[customer]['q2']
            q3_total += data[customer]['q3']
            q4_total += data[customer]['q4']
            sale_total += (data[customer]['q1'] + data[customer]['q2'] + data[customer]['q3'] + data[customer]['q4'])
        context = super().get_context_data(**kwargs)
        context['sale_data'] = data
        context['first_col'] = 'customer'
        context['region'] = sales[0].location.region
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['sale_total'] = sale_total
        return context

#################################################
########## ACTUALS BY REGION BY SECTOR ##########
#################################################

class ChooseLocationSaleRegionSector(ChooseLocationView):
    def get_context_data(self, **kwargs):
        regions = {sale.location.region for sale in Sale.objects.all().order_by('location__name')}
        context = super().get_context_data(**kwargs)
        context['locations'] = regions
        context['redirect'] = 'cy_sale_region_sector'
        return context

class ChooseYearSaleRegionSector(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {sale.year for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['location_name_slug'] = self.kwargs['region_name_slug']
        context['redirect'] = 'sale_region_sector'
        return context

class SaleRegionSector(SaleView):
    def get_context_data(self, **kwargs):
        sales = Sale.objects.filter(
            location__region__slug=self.kwargs['region_name_slug'],
            year=self.kwargs['year']
        ).order_by('customer__sector')
        data = {}
        for sale in sales:
            if sale.customer.sector not in data.keys():
                data[sale.customer.sector] = {
                    'jan': sale.jan,
                    'feb': sale.feb,
                    'mar': sale.mar,
                    'apr': sale.apr,
                    'may': sale.may,
                    'jun': sale.jun,
                    'jul': sale.jul,
                    'aug': sale.aug,
                    'sep': sale.sep,
                    'oct': sale.oct,
                    'nov': sale.nov,
                    'dec': sale.dec,
                    'q1': sale.q1,
                    'q2': sale.q2,
                    'q3': sale.q3,
                    'q4': sale.q4,
                }
            else:
                data[sale.customer.sector]['jan'] += sale.jan
                data[sale.customer.sector]['feb'] += sale.feb
                data[sale.customer.sector]['mar'] += sale.mar
                data[sale.customer.sector]['apr'] += sale.apr
                data[sale.customer.sector]['may'] += sale.may
                data[sale.customer.sector]['jun'] += sale.jun
                data[sale.customer.sector]['jul'] += sale.jul
                data[sale.customer.sector]['aug'] += sale.aug
                data[sale.customer.sector]['sep'] += sale.sep
                data[sale.customer.sector]['oct'] += sale.oct
                data[sale.customer.sector]['nov'] += sale.nov
                data[sale.customer.sector]['dec'] += sale.dec
                data[sale.customer.sector]['q1'] += sale.q1
                data[sale.customer.sector]['q2'] += sale.q2
                data[sale.customer.sector]['q3'] += sale.q3
                data[sale.customer.sector]['q4'] += sale.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        sale_total = 0
        for sector in data:
            jan_total += data[sector]['jan']
            feb_total += data[sector]['feb']
            mar_total += data[sector]['mar']
            apr_total += data[sector]['apr']
            may_total += data[sector]['may']
            jun_total += data[sector]['jun']
            jul_total += data[sector]['jul']
            aug_total += data[sector]['aug']
            sep_total += data[sector]['sep']
            oct_total += data[sector]['oct']
            nov_total += data[sector]['nov']
            dec_total += data[sector]['dec']
            q1_total += data[sector]['q1']
            q2_total += data[sector]['q2']
            q3_total += data[sector]['q3']
            q4_total += data[sector]['q4']
            sale_total += (data[sector]['q1'] + data[sector]['q2'] + data[sector]['q3'] + data[sector]['q4'])
        context = super().get_context_data(**kwargs)
        context['sale_data'] = data
        context['first_col'] = 'sector'
        context['region'] = sales[0].location.region
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['sale_total'] = sale_total
        return context

###########################################
########## GLOBAL SALES BY PLANT ##########
###########################################

class ChooseYearSaleGlobalPlant(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {sale.year for sale in Sale.objects.all().order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'sale_global_plant'
        return context

class SaleGlobalPlant(SaleView):
    def get_context_data(self, **kwargs):
        sales = Sale.objects.filter(
            year=self.kwargs['year']
        ).order_by('location__name')
        data = {}
        for sale in sales:
            if sale.location not in data.keys():
                data[sale.location] = {
                    'jan': sale.jan,
                    'feb': sale.feb,
                    'mar': sale.mar,
                    'apr': sale.apr,
                    'may': sale.may,
                    'jun': sale.jun,
                    'jul': sale.jul,
                    'aug': sale.aug,
                    'sep': sale.sep,
                    'oct': sale.oct,
                    'nov': sale.nov,
                    'dec': sale.dec,
                    'q1': sale.q1,
                    'q2': sale.q2,
                    'q3': sale.q3,
                    'q4': sale.q4,
                }
            else:
                data[sale.location]['jan'] += sale.jan
                data[sale.location]['feb'] += sale.feb
                data[sale.location]['mar'] += sale.mar
                data[sale.location]['apr'] += sale.apr
                data[sale.location]['may'] += sale.may
                data[sale.location]['jun'] += sale.jun
                data[sale.location]['jul'] += sale.jul
                data[sale.location]['aug'] += sale.aug
                data[sale.location]['sep'] += sale.sep
                data[sale.location]['oct'] += sale.oct
                data[sale.location]['nov'] += sale.nov
                data[sale.location]['dec'] += sale.dec
                data[sale.location]['q1'] += sale.q1
                data[sale.location]['q2'] += sale.q2
                data[sale.location]['q3'] += sale.q3
                data[sale.location]['q4'] += sale.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        sale_total = 0
        for plant in data:
            jan_total += data[plant]['jan']
            feb_total += data[plant]['feb']
            mar_total += data[plant]['mar']
            apr_total += data[plant]['apr']
            may_total += data[plant]['may']
            jun_total += data[plant]['jun']
            jul_total += data[plant]['jul']
            aug_total += data[plant]['aug']
            sep_total += data[plant]['sep']
            oct_total += data[plant]['oct']
            nov_total += data[plant]['nov']
            dec_total += data[plant]['dec']
            q1_total += data[plant]['q1']
            q2_total += data[plant]['q2']
            q3_total += data[plant]['q3']
            q4_total += data[plant]['q4']
            sale_total += (data[plant]['q1'] + data[plant]['q2'] + data[plant]['q3'] + data[plant]['q4'])
        context = super().get_context_data(**kwargs)
        context['sale_data'] = data
        context['global'] = True
        context['first_col'] = 'plant'
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['sale_total'] = sale_total
        return context

##############################################
########## GLOBAL SALES BY CUSTOMER ##########
##############################################

class ChooseYearSaleGlobalCustomer(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {sale.year for sale in Sale.objects.all().order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'sale_global_customer'
        return context

class SaleGlobalCustomer(SaleView):
    def get_context_data(self, **kwargs):
        sales = Sale.objects.filter(
            year=self.kwargs['year']
        ).order_by('customer__name')
        data = {}
        for sale in sales:
            if sale.customer not in data.keys():
                data[sale.customer] = {
                    'jan': sale.jan,
                    'feb': sale.feb,
                    'mar': sale.mar,
                    'apr': sale.apr,
                    'may': sale.may,
                    'jun': sale.jun,
                    'jul': sale.jul,
                    'aug': sale.aug,
                    'sep': sale.sep,
                    'oct': sale.oct,
                    'nov': sale.nov,
                    'dec': sale.dec,
                    'q1': sale.q1,
                    'q2': sale.q2,
                    'q3': sale.q3,
                    'q4': sale.q4,
                }
            else:
                data[sale.customer]['jan'] += sale.jan
                data[sale.customer]['feb'] += sale.feb
                data[sale.customer]['mar'] += sale.mar
                data[sale.customer]['apr'] += sale.apr
                data[sale.customer]['may'] += sale.may
                data[sale.customer]['jun'] += sale.jun
                data[sale.customer]['jul'] += sale.jul
                data[sale.customer]['aug'] += sale.aug
                data[sale.customer]['sep'] += sale.sep
                data[sale.customer]['oct'] += sale.oct
                data[sale.customer]['nov'] += sale.nov
                data[sale.customer]['dec'] += sale.dec
                data[sale.customer]['q1'] += sale.q1
                data[sale.customer]['q2'] += sale.q2
                data[sale.customer]['q3'] += sale.q3
                data[sale.customer]['q4'] += sale.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        sale_total = 0
        for customer in data:
            jan_total += data[customer]['jan']
            feb_total += data[customer]['feb']
            mar_total += data[customer]['mar']
            apr_total += data[customer]['apr']
            may_total += data[customer]['may']
            jun_total += data[customer]['jun']
            jul_total += data[customer]['jul']
            aug_total += data[customer]['aug']
            sep_total += data[customer]['sep']
            oct_total += data[customer]['oct']
            nov_total += data[customer]['nov']
            dec_total += data[customer]['dec']
            q1_total += data[customer]['q1']
            q2_total += data[customer]['q2']
            q3_total += data[customer]['q3']
            q4_total += data[customer]['q4']
            sale_total += (data[customer]['q1'] + data[customer]['q2'] + data[customer]['q3'] + data[customer]['q4'])
        context = super().get_context_data(**kwargs)
        context['sale_data'] = data
        context['global'] = True
        context['first_col'] = 'customer'
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['sale_total'] = sale_total
        return context

############################################
########## GLOBAL SALES BY SECTOR ##########
############################################

class ChooseYearSaleGlobalSector(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {sale.year for sale in Sale.objects.all().order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'sale_global_sector'
        return context

class SaleGlobalSector(SaleView):
    def get_context_data(self, **kwargs):
        sales = Sale.objects.filter(
            year=self.kwargs['year']
        ).order_by('customer__sector')
        data = {}
        for sale in sales:
            if sale.customer.sector not in data.keys():
                data[sale.customer.sector] = {
                    'jan': sale.jan,
                    'feb': sale.feb,
                    'mar': sale.mar,
                    'apr': sale.apr,
                    'may': sale.may,
                    'jun': sale.jun,
                    'jul': sale.jul,
                    'aug': sale.aug,
                    'sep': sale.sep,
                    'oct': sale.oct,
                    'nov': sale.nov,
                    'dec': sale.dec,
                    'q1': sale.q1,
                    'q2': sale.q2,
                    'q3': sale.q3,
                    'q4': sale.q4,
                }
            else:
                data[sale.customer.sector]['jan'] += sale.jan
                data[sale.customer.sector]['feb'] += sale.feb
                data[sale.customer.sector]['mar'] += sale.mar
                data[sale.customer.sector]['apr'] += sale.apr
                data[sale.customer.sector]['may'] += sale.may
                data[sale.customer.sector]['jun'] += sale.jun
                data[sale.customer.sector]['jul'] += sale.jul
                data[sale.customer.sector]['aug'] += sale.aug
                data[sale.customer.sector]['sep'] += sale.sep
                data[sale.customer.sector]['oct'] += sale.oct
                data[sale.customer.sector]['nov'] += sale.nov
                data[sale.customer.sector]['dec'] += sale.dec
                data[sale.customer.sector]['q1'] += sale.q1
                data[sale.customer.sector]['q2'] += sale.q2
                data[sale.customer.sector]['q3'] += sale.q3
                data[sale.customer.sector]['q4'] += sale.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        sale_total = 0
        for sector in data:
            jan_total += data[sector]['jan']
            feb_total += data[sector]['feb']
            mar_total += data[sector]['mar']
            apr_total += data[sector]['apr']
            may_total += data[sector]['may']
            jun_total += data[sector]['jun']
            jul_total += data[sector]['jul']
            aug_total += data[sector]['aug']
            sep_total += data[sector]['sep']
            oct_total += data[sector]['oct']
            nov_total += data[sector]['nov']
            dec_total += data[sector]['dec']
            q1_total += data[sector]['q1']
            q2_total += data[sector]['q2']
            q3_total += data[sector]['q3']
            q4_total += data[sector]['q4']
            sale_total += (data[sector]['q1'] + data[sector]['q2'] + data[sector]['q3'] + data[sector]['q4'])
        context = super().get_context_data(**kwargs)
        context['sale_data'] = data
        context['global'] = True
        context['first_col'] = 'sector'
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['sale_total'] = sale_total
        return context

############################################
########## GLOBAL SALES BY REGION ##########
############################################

class ChooseYearSaleGlobalRegion(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {sale.year for sale in Sale.objects.all().order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'sale_global_region'
        return context

class SaleGlobalRegion(SaleView):
    def get_context_data(self, **kwargs):
        sales = Sale.objects.filter(
            year=self.kwargs['year']
        ).order_by('location__region')
        data = {}
        for sale in sales:
            if sale.location.region not in data.keys():
                data[sale.location.region] = {
                    'jan': sale.jan,
                    'feb': sale.feb,
                    'mar': sale.mar,
                    'apr': sale.apr,
                    'may': sale.may,
                    'jun': sale.jun,
                    'jul': sale.jul,
                    'aug': sale.aug,
                    'sep': sale.sep,
                    'oct': sale.oct,
                    'nov': sale.nov,
                    'dec': sale.dec,
                    'q1': sale.q1,
                    'q2': sale.q2,
                    'q3': sale.q3,
                    'q4': sale.q4,
                }
            else:
                data[sale.location.region]['jan'] += sale.jan
                data[sale.location.region]['feb'] += sale.feb
                data[sale.location.region]['mar'] += sale.mar
                data[sale.location.region]['apr'] += sale.apr
                data[sale.location.region]['may'] += sale.may
                data[sale.location.region]['jun'] += sale.jun
                data[sale.location.region]['jul'] += sale.jul
                data[sale.location.region]['aug'] += sale.aug
                data[sale.location.region]['sep'] += sale.sep
                data[sale.location.region]['oct'] += sale.oct
                data[sale.location.region]['nov'] += sale.nov
                data[sale.location.region]['dec'] += sale.dec
                data[sale.location.region]['q1'] += sale.q1
                data[sale.location.region]['q2'] += sale.q2
                data[sale.location.region]['q3'] += sale.q3
                data[sale.location.region]['q4'] += sale.q4
        jan_total, feb_total, mar_total = 0, 0, 0
        apr_total, may_total, jun_total = 0, 0, 0
        jul_total, aug_total, sep_total = 0, 0, 0
        oct_total, nov_total, dec_total = 0, 0, 0
        q1_total, q2_total, q3_total, q4_total = 0, 0, 0, 0
        sale_total = 0
        for region in data:
            jan_total += data[region]['jan']
            feb_total += data[region]['feb']
            mar_total += data[region]['mar']
            apr_total += data[region]['apr']
            may_total += data[region]['may']
            jun_total += data[region]['jun']
            jul_total += data[region]['jul']
            aug_total += data[region]['aug']
            sep_total += data[region]['sep']
            oct_total += data[region]['oct']
            nov_total += data[region]['nov']
            dec_total += data[region]['dec']
            q1_total += data[region]['q1']
            q2_total += data[region]['q2']
            q3_total += data[region]['q3']
            q4_total += data[region]['q4']
            sale_total += (data[region]['q1'] + data[region]['q2'] + data[region]['q3'] + data[region]['q4'])
        context = super().get_context_data(**kwargs)
        context['sale_data'] = data
        context['global'] = True
        context['first_col'] = 'region'
        context['year'] = self.kwargs['year']
        context['jan_total'] = jan_total
        context['feb_total'] = feb_total
        context['mar_total'] = mar_total
        context['apr_total'] = apr_total
        context['may_total'] = may_total
        context['jun_total'] = jun_total
        context['jul_total'] = jul_total
        context['aug_total'] = aug_total
        context['sep_total'] = sep_total
        context['oct_total'] = oct_total
        context['nov_total'] = nov_total
        context['dec_total'] = dec_total
        context['q1_total'] = q1_total
        context['q2_total'] = q2_total
        context['q3_total'] = q3_total
        context['q4_total'] = q4_total
        context['sale_total'] = sale_total
        return context

######################################
########## EDIT BUDGET FORM ##########
######################################

class BudgetFormChooseLocation(ChooseLocationView):
    def get_context_data(self, **kwargs):
        locations = {budget.location for budget in Budget.objects.all()}
        context = super().get_context_data(**kwargs)
        context['locations'] = locations
        context['redirect'] = 'cy_budget_form'
        return context

class BudgetFormChooseYear(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {budget.year for budget in Budget.objects.filter(
            location__slug=self.kwargs['location_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['location_name_slug'] = self.kwargs['location_name_slug']
        context['redirect'] = 'budget_form'
        return context

### TO DO ###
# breadcrumbs
 
### Questions ###
# should finished budget form be cloned for sales? ***yes***

@login_required
def form_budget(request, location_name_slug, year):
    location = Location.objects.get(slug=location_name_slug)
    BudgetInlineFormSet = inlineformset_factory(Location, Budget, fields=(
        'customer', 'jan', 'feb',
        'mar', 'apr', 'may', 'jun',
        'jul', 'aug', 'sep', 'oct',
        'nov', 'dec', 'year',
    ), extra=0, min_num=1)
    if request.method == 'POST':
        formset = BudgetInlineFormSet(request.POST, instance=location)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Budget updated successfully.")
            return HttpResponseRedirect('')
    else:
        print('INVALID' * 3, location)
        formset = BudgetInlineFormSet(instance=location)
    return render(request, 'Ledger/budget_form.html', {'formset': formset, 'location': location, 'year': year})

###########################################
########## A VS B CUSTOMER PLANT ##########
###########################################

class ChooseCustomerVsCustomerPlant(ChooseCustomerView):
    def get_context_data(self, **kwargs):
        customers = {
            budget.customer for budget in Budget.objects.all()
        } & {
            sale.customer for sale in Sale.objects.all()
        }
        context = super().get_context_data(**kwargs)
        context['redirect'] = 'cy_vs_customer_plant'
        context['object_list'] = customers
        return context

class ChooseYearVsCustomerPlant(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {
            budget.year for budget in Budget.objects.filter(customer__slug=self.kwargs['customer_name_slug'])
        } & {
            sale.year for sale in Sale.objects.filter(customer__slug=self.kwargs['customer_name_slug'])
        }
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['customer'] = self.kwargs['customer_name_slug']
        context['redirect'] = 'cq_vs_customer_plant'
        return context

class ChooseQuarterVsCustomerPlant(ChooseQuarterView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quarters'] = ['q1', 'q2', 'q3', 'q4']
        context['redirect'] = 'vs_customer_plant'
        return context

class VsCustomerPlant(VersusView):
    def get_context_data(self, **kwargs):
        customer = Customer.objects.get(slug=self.kwargs['customer_name_slug'])
        plants = {
            budget.location for budget in Budget.objects.filter(customer=customer)
        } & {
            sale.location for sale in Sale.objects.filter(customer=customer)
        }
        if self.kwargs['q'] == 'q1':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for plant in plants:
                data[plant] = {
                    'jan': {
                        'budget': Budget.objects.get(customer=customer, location=plant).jan,
                        'actual': Sale.objects.get(customer=customer, location=plant).jan,
                    },
                    'feb': {
                        'budget': Budget.objects.get(customer=customer, location=plant).feb,
                        'actual': Sale.objects.get(customer=customer, location=plant).feb,
                    },
                    'mar': {
                        'budget': Budget.objects.get(customer=customer, location=plant).mar,
                        'actual': Sale.objects.get(customer=customer, location=plant).mar,
                    },
                }
                data['totals']['actual'] += data[plant]['jan']['actual']
                data['totals']['actual'] += data[plant]['feb']['actual']
                data['totals']['actual'] += data[plant]['mar']['actual']
                data['totals']['budget'] += data[plant]['jan']['budget']
                data['totals']['budget'] += data[plant]['feb']['budget']
                data['totals']['budget'] += data[plant]['mar']['budget']
            totals = {
                'jan_actual': 0,
                'jan_budget': 0,
                'feb_actual': 0,
                'feb_budget': 0,
                'mar_actual': 0,
                'mar_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jan_actual'] += value['jan']['actual']
                    totals['jan_budget'] += value['jan']['budget']
                    totals['feb_actual'] += value['feb']['actual']
                    totals['feb_budget'] += value['feb']['budget']
                    totals['mar_actual'] += value['mar']['actual']
                    totals['mar_budget'] += value['mar']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'plant'
            context['data'] = data
            context['customer'] = customer
            context['totals'] = totals
            context['q'] = 'Q1'
        
        elif self.kwargs['q'] == 'q2':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for plant in plants:
                data[plant] = {
                    'apr': {
                        'budget': Budget.objects.get(customer=customer, location=plant).apr,
                        'actual': Sale.objects.get(customer=customer, location=plant).apr,
                    },
                    'may': {
                        'budget': Budget.objects.get(customer=customer, location=plant).may,
                        'actual': Sale.objects.get(customer=customer, location=plant).may,
                    },
                    'jun': {
                        'budget': Budget.objects.get(customer=customer, location=plant).jun,
                        'actual': Sale.objects.get(customer=customer, location=plant).jun,
                    },
                }
                data['totals']['actual'] += data[plant]['apr']['actual']
                data['totals']['actual'] += data[plant]['may']['actual']
                data['totals']['actual'] += data[plant]['jun']['actual']
                data['totals']['budget'] += data[plant]['apr']['budget']
                data['totals']['budget'] += data[plant]['may']['budget']
                data['totals']['budget'] += data[plant]['jun']['budget']
            totals = {
                'apr_actual': 0,
                'apr_budget': 0,
                'may_actual': 0,
                'may_budget': 0,
                'jun_actual': 0,
                'jun_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['apr_actual'] += value['apr']['actual']
                    totals['apr_budget'] += value['apr']['budget']
                    totals['may_actual'] += value['may']['actual']
                    totals['may_budget'] += value['may']['budget']
                    totals['jun_actual'] += value['jun']['actual']
                    totals['jun_budget'] += value['jun']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'plant'
            context['data'] = data
            context['customer'] = customer
            context['totals'] = totals
            context['q'] = 'Q2'

        elif self.kwargs['q'] == 'q3':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for plant in plants:
                data[plant] = {
                    'jul': {
                        'budget': Budget.objects.get(customer=customer, location=plant).jul,
                        'actual': Sale.objects.get(customer=customer, location=plant).jul,
                    },
                    'aug': {
                        'budget': Budget.objects.get(customer=customer, location=plant).aug,
                        'actual': Sale.objects.get(customer=customer, location=plant).aug,
                    },
                    'sep': {
                        'budget': Budget.objects.get(customer=customer, location=plant).sep,
                        'actual': Sale.objects.get(customer=customer, location=plant).sep,
                    },
                }
                data['totals']['actual'] += data[plant]['jul']['actual']
                data['totals']['actual'] += data[plant]['aug']['actual']
                data['totals']['actual'] += data[plant]['sep']['actual']
                data['totals']['budget'] += data[plant]['jul']['budget']
                data['totals']['budget'] += data[plant]['aug']['budget']
                data['totals']['budget'] += data[plant]['sep']['budget']
            totals = {
                'jul_actual': 0,
                'jul_budget': 0,
                'aug_actual': 0,
                'aug_budget': 0,
                'sep_actual': 0,
                'sep_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jul_actual'] += value['jul']['actual']
                    totals['jul_budget'] += value['jul']['budget']
                    totals['aug_actual'] += value['aug']['actual']
                    totals['aug_budget'] += value['aug']['budget']
                    totals['sep_actual'] += value['sep']['actual']
                    totals['sep_budget'] += value['sep']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'plant'
            context['data'] = data
            context['customer'] = customer
            context['totals'] = totals
            context['q'] = 'Q3'

        elif self.kwargs['q'] == 'q4':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for plant in plants:
                data[plant] = {
                    'oct': {
                        'budget': Budget.objects.get(customer=customer, location=plant).oct,
                        'actual': Sale.objects.get(customer=customer, location=plant).oct,
                    },
                    'nov': {
                        'budget': Budget.objects.get(customer=customer, location=plant).nov,
                        'actual': Sale.objects.get(customer=customer, location=plant).nov,
                    },
                    'dec': {
                        'budget': Budget.objects.get(customer=customer, location=plant).dec,
                        'actual': Sale.objects.get(customer=customer, location=plant).dec,
                    },
                }
                data['totals']['actual'] += data[plant]['oct']['actual']
                data['totals']['actual'] += data[plant]['nov']['actual']
                data['totals']['actual'] += data[plant]['dec']['actual']
                data['totals']['budget'] += data[plant]['oct']['budget']
                data['totals']['budget'] += data[plant]['nov']['budget']
                data['totals']['budget'] += data[plant]['dec']['budget']
            totals = {
                'oct_actual': 0,
                'oct_budget': 0,
                'nov_actual': 0,
                'nov_budget': 0,
                'dec_actual': 0,
                'dec_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['oct_actual'] += value['oct']['actual']
                    totals['oct_budget'] += value['oct']['budget']
                    totals['nov_actual'] += value['nov']['actual']
                    totals['nov_budget'] += value['nov']['budget']
                    totals['dec_actual'] += value['dec']['actual']
                    totals['dec_budget'] += value['dec']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'plant'
            context['data'] = data
            context['customer'] = customer
            context['totals'] = totals
            context['q'] = 'Q4'
        else:
            pass
        return context

###########################################
########## A VS B PLANT CUSTOMER ##########
###########################################

class ChooseLocationVsPlantCustomer(ChooseLocationView):
    def get_context_data(self, **kwargs):
        locations = {
            budget.location for budget in Budget.objects.all()
        } & {
            sale.location for sale in Sale.objects.all()
        }
        context = super().get_context_data(**kwargs)
        context['locations'] = locations
        context['redirect'] = 'cy_vs_plant_customer'
        return context

class ChooseYearVsPlantCustomer(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {
            budget.year for budget in Budget.objects.filter(location__slug=self.kwargs['location_name_slug'])
        } & {
            sale.year for sale in Sale.objects.filter(location__slug=self.kwargs['location_name_slug'])
        }
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'cq_vs_plant_customer'
        return context

class ChooseQuarterVsPlantCustomer(ChooseQuarterView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quarters'] = ['q1', 'q2', 'q3', 'q4']
        context['redirect'] = 'vs_plant_customer'
        return context

class VsPlantCustomer(VersusView):
    def get_context_data(self, **kwargs):
        plant = Location.objects.get(slug=self.kwargs['location_name_slug'])
        customers = {
            budget.customer for budget in Budget.objects.filter(location=plant)
        } & {
            sale.customer for sale in Sale.objects.filter(location=plant)
        }
        if self.kwargs['q'] == 'q1':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for customer in customers:
                data[customer] = {
                    'jan': {
                        'budget': Budget.objects.get(customer=customer, location=plant).jan,
                        'actual': Sale.objects.get(customer=customer, location=plant).jan,
                    },
                    'feb': {
                        'budget': Budget.objects.get(customer=customer, location=plant).feb,
                        'actual': Sale.objects.get(customer=customer, location=plant).feb,
                    },
                    'mar': {
                        'budget': Budget.objects.get(customer=customer, location=plant).mar,
                        'actual': Sale.objects.get(customer=customer, location=plant).mar,
                    },
                }
                data['totals']['actual'] += data[customer]['jan']['actual']
                data['totals']['actual'] += data[customer]['feb']['actual']
                data['totals']['actual'] += data[customer]['mar']['actual']
                data['totals']['budget'] += data[customer]['jan']['budget']
                data['totals']['budget'] += data[customer]['feb']['budget']
                data['totals']['budget'] += data[customer]['mar']['budget']
            totals = {
                'jan_actual': 0,
                'jan_budget': 0,
                'feb_actual': 0,
                'feb_budget': 0,
                'mar_actual': 0,
                'mar_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jan_actual'] += value['jan']['actual']
                    totals['jan_budget'] += value['jan']['budget']
                    totals['feb_actual'] += value['feb']['actual']
                    totals['feb_budget'] += value['feb']['budget']
                    totals['mar_actual'] += value['mar']['actual']
                    totals['mar_budget'] += value['mar']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'customer'
            context['data'] = data
            context['plant'] = plant
            context['totals'] = totals
            context['q'] = 'Q1'

        elif self.kwargs['q'] == 'q2':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for customer in customers:
                data[customer] = {
                    'apr': {
                        'budget': Budget.objects.get(customer=customer, location=plant).apr,
                        'actual': Sale.objects.get(customer=customer, location=plant).apr,
                    },
                    'may': {
                        'budget': Budget.objects.get(customer=customer, location=plant).may,
                        'actual': Sale.objects.get(customer=customer, location=plant).may,
                    },
                    'jun': {
                        'budget': Budget.objects.get(customer=customer, location=plant).jun,
                        'actual': Sale.objects.get(customer=customer, location=plant).jun,
                    },
                }
                data['totals']['actual'] += data[customer]['apr']['actual']
                data['totals']['actual'] += data[customer]['may']['actual']
                data['totals']['actual'] += data[customer]['jun']['actual']
                data['totals']['budget'] += data[customer]['apr']['budget']
                data['totals']['budget'] += data[customer]['may']['budget']
                data['totals']['budget'] += data[customer]['jun']['budget']
            totals = {
                'apr_actual': 0,
                'apr_budget': 0,
                'may_actual': 0,
                'may_budget': 0,
                'jun_actual': 0,
                'jun_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['apr_actual'] += value['apr']['actual']
                    totals['apr_budget'] += value['apr']['budget']
                    totals['may_actual'] += value['may']['actual']
                    totals['may_budget'] += value['may']['budget']
                    totals['jun_actual'] += value['jun']['actual']
                    totals['jun_budget'] += value['jun']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'customer'
            context['data'] = data
            context['plant'] = plant
            context['totals'] = totals
            context['q'] = 'Q2'

        elif self.kwargs['q'] == 'q3':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for customer in customers:
                data[customer] = {
                    'jul': {
                        'budget': Budget.objects.get(customer=customer, location=plant).jul,
                        'actual': Sale.objects.get(customer=customer, location=plant).jul,
                    },
                    'aug': {
                        'budget': Budget.objects.get(customer=customer, location=plant).aug,
                        'actual': Sale.objects.get(customer=customer, location=plant).aug,
                    },
                    'sep': {
                        'budget': Budget.objects.get(customer=customer, location=plant).sep,
                        'actual': Sale.objects.get(customer=customer, location=plant).sep,
                    },
                }
                data['totals']['actual'] += data[customer]['jul']['actual']
                data['totals']['actual'] += data[customer]['aug']['actual']
                data['totals']['actual'] += data[customer]['sep']['actual']
                data['totals']['budget'] += data[customer]['jul']['budget']
                data['totals']['budget'] += data[customer]['aug']['budget']
                data['totals']['budget'] += data[customer]['sep']['budget']
            totals = {
                'jul_actual': 0,
                'jul_budget': 0,
                'aug_actual': 0,
                'aug_budget': 0,
                'sep_actual': 0,
                'sep_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jul_actual'] += value['jul']['actual']
                    totals['jul_budget'] += value['jul']['budget']
                    totals['aug_actual'] += value['aug']['actual']
                    totals['aug_budget'] += value['aug']['budget']
                    totals['sep_actual'] += value['sep']['actual']
                    totals['sep_budget'] += value['sep']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'customer'
            context['data'] = data
            context['plant'] = plant
            context['totals'] = totals
            context['q'] = 'Q3'
        
        elif self.kwargs['q'] == 'q4':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for customer in customers:
                data[customer] = {
                    'oct': {
                        'budget': Budget.objects.get(customer=customer, location=plant).oct,
                        'actual': Sale.objects.get(customer=customer, location=plant).oct,
                    },
                    'nov': {
                        'budget': Budget.objects.get(customer=customer, location=plant).nov,
                        'actual': Sale.objects.get(customer=customer, location=plant).nov,
                    },
                    'dec': {
                        'budget': Budget.objects.get(customer=customer, location=plant).dec,
                        'actual': Sale.objects.get(customer=customer, location=plant).dec,
                    },
                }
                data['totals']['actual'] += data[customer]['oct']['actual']
                data['totals']['actual'] += data[customer]['nov']['actual']
                data['totals']['actual'] += data[customer]['dec']['actual']
                data['totals']['budget'] += data[customer]['oct']['budget']
                data['totals']['budget'] += data[customer]['nov']['budget']
                data['totals']['budget'] += data[customer]['dec']['budget']
            totals = {
                'oct_actual': 0,
                'oct_budget': 0,
                'nov_actual': 0,
                'nov_budget': 0,
                'dec_actual': 0,
                'dec_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['oct_actual'] += value['oct']['actual']
                    totals['oct_budget'] += value['oct']['budget']
                    totals['nov_actual'] += value['nov']['actual']
                    totals['nov_budget'] += value['nov']['budget']
                    totals['dec_actual'] += value['dec']['actual']
                    totals['dec_budget'] += value['dec']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'customer'
            context['data'] = data
            context['plant'] = plant
            context['totals'] = totals
            context['q'] = 'Q4'
        else:
            pass
        return context

#########################################
########## A VS B PLANT SECTOR ##########
#########################################

class ChooseLocationVsPlantSector(ChooseLocationView):
    def get_context_data(self, **kwargs):
        locations = {
            budget.location for budget in Budget.objects.all()
        } & {
            sale.location for sale in Sale.objects.all()
        }
        context = super().get_context_data(**kwargs)
        context['locations'] = locations
        context['redirect'] = 'cy_vs_plant_sector'
        return context

class ChooseYearVsPlantSector(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {
            budget.year for budget in Budget.objects.filter(location__slug=self.kwargs['location_name_slug'])
        } & {
            sale.year for sale in Sale.objects.filter(location__slug=self.kwargs['location_name_slug'])
        }
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'cq_vs_plant_sector'
        return context

class ChooseQuarterVsPlantSector(ChooseQuarterView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quarters'] = ['q1', 'q2', 'q3', 'q4']
        context['redirect'] = 'vs_plant_sector'
        return context

class VsPlantSector(VersusView):
    def get_context_data(self, **kwargs):
        plant = Location.objects.get(slug=self.kwargs['location_name_slug'])
        sectors = {
            budget.customer.sector for budget in Budget.objects.filter(location=plant)
        } & {
            sale.customer.sector for sale in Sale.objects.filter(location=plant)
        }
        print(sectors)
        if self.kwargs['q'] == 'q1':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for sector in sectors:
                data[sector] = {
                    'jan': {
                        'budget': 0,
                        'actual': 0
                    },
                    'feb': {
                        'budget': 0,
                        'actual': 0
                    },
                    'mar': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(customer__sector=sector, location=plant):
                    data[sector]['jan']['budget'] += budget.jan
                    data[sector]['feb']['budget'] += budget.feb
                    data[sector]['mar']['budget'] += budget.mar
                for sale in Sale.objects.filter(customer__sector=sector, location=plant):
                    data[sector]['jan']['actual'] += sale.jan
                    data[sector]['feb']['actual'] += sale.feb
                    data[sector]['mar']['actual'] += sale.mar
                data['totals']['actual'] += data[sector]['jan']['actual']
                data['totals']['actual'] += data[sector]['feb']['actual']
                data['totals']['actual'] += data[sector]['mar']['actual']
                data['totals']['budget'] += data[sector]['jan']['budget']
                data['totals']['budget'] += data[sector]['feb']['budget']
                data['totals']['budget'] += data[sector]['mar']['budget']
            totals = {
                'jan_actual': 0,
                'jan_budget': 0,
                'feb_actual': 0,
                'feb_budget': 0,
                'mar_actual': 0,
                'mar_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jan_actual'] += value['jan']['actual']
                    totals['jan_budget'] += value['jan']['budget']
                    totals['feb_actual'] += value['feb']['actual']
                    totals['feb_budget'] += value['feb']['budget']
                    totals['mar_actual'] += value['mar']['actual']
                    totals['mar_budget'] += value['mar']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'sector'
            context['data'] = data
            context['plant'] = plant
            context['totals'] = totals
            context['q'] = 'Q1'

        elif self.kwargs['q'] == 'q2':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for sector in sectors:
                data[sector] = {
                    'apr': {
                        'budget': 0,
                        'actual': 0
                    },
                    'may': {
                        'budget': 0,
                        'actual': 0
                    },
                    'jun': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(customer__sector=sector, location=plant):
                    data[sector]['apr']['budget'] += budget.apr
                    data[sector]['may']['budget'] += budget.may
                    data[sector]['jun']['budget'] += budget.jun
                for sale in Sale.objects.filter(customer__sector=sector, location=plant):
                    data[sector]['apr']['actual'] += sale.apr
                    data[sector]['may']['actual'] += sale.may
                    data[sector]['jun']['actual'] += sale.jun
                data['totals']['actual'] += data[sector]['apr']['actual']
                data['totals']['actual'] += data[sector]['may']['actual']
                data['totals']['actual'] += data[sector]['jun']['actual']
                data['totals']['budget'] += data[sector]['apr']['budget']
                data['totals']['budget'] += data[sector]['may']['budget']
                data['totals']['budget'] += data[sector]['jun']['budget']
            totals = {
                'apr_actual': 0,
                'apr_budget': 0,
                'may_actual': 0,
                'may_budget': 0,
                'jun_actual': 0,
                'jun_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['apr_actual'] += value['apr']['actual']
                    totals['apr_budget'] += value['apr']['budget']
                    totals['may_actual'] += value['may']['actual']
                    totals['may_budget'] += value['may']['budget']
                    totals['jun_actual'] += value['jun']['actual']
                    totals['jun_budget'] += value['jun']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'sector'
            context['data'] = data
            context['plant'] = plant
            context['totals'] = totals
            context['q'] = 'Q2'

        elif self.kwargs['q'] == 'q3':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for sector in sectors:
                data[sector] = {
                    'jul': {
                        'budget': 0,
                        'actual': 0
                    },
                    'aug': {
                        'budget': 0,
                        'actual': 0
                    },
                    'sep': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(customer__sector=sector, location=plant):
                    data[sector]['jul']['budget'] += budget.jul
                    data[sector]['aug']['budget'] += budget.aug
                    data[sector]['sep']['budget'] += budget.sep
                for sale in Sale.objects.filter(customer__sector=sector, location=plant):
                    data[sector]['jul']['actual'] += sale.jul
                    data[sector]['aug']['actual'] += sale.aug
                    data[sector]['sep']['actual'] += sale.sep
                data['totals']['actual'] += data[sector]['jul']['actual']
                data['totals']['actual'] += data[sector]['aug']['actual']
                data['totals']['actual'] += data[sector]['sep']['actual']
                data['totals']['budget'] += data[sector]['jul']['budget']
                data['totals']['budget'] += data[sector]['aug']['budget']
                data['totals']['budget'] += data[sector]['sep']['budget']
            totals = {
                'jul_actual': 0,
                'jul_budget': 0,
                'aug_actual': 0,
                'aug_budget': 0,
                'sep_actual': 0,
                'sep_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jul_actual'] += value['jul']['actual']
                    totals['jul_budget'] += value['jul']['budget']
                    totals['aug_actual'] += value['aug']['actual']
                    totals['aug_budget'] += value['aug']['budget']
                    totals['sep_actual'] += value['sep']['actual']
                    totals['sep_budget'] += value['sep']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'sector'
            context['data'] = data
            context['plant'] = plant
            context['totals'] = totals
            context['q'] = 'Q3'

        elif self.kwargs['q'] == 'q4':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for sector in sectors:
                data[sector] = {
                    'oct': {
                        'budget': 0,
                        'actual': 0
                    },
                    'nov': {
                        'budget': 0,
                        'actual': 0
                    },
                    'dec': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(customer__sector=sector, location=plant):
                    data[sector]['oct']['budget'] += budget.oct
                    data[sector]['nov']['budget'] += budget.nov
                    data[sector]['dec']['budget'] += budget.dec
                for sale in Sale.objects.filter(customer__sector=sector, location=plant):
                    data[sector]['oct']['actual'] += sale.oct
                    data[sector]['nov']['actual'] += sale.nov
                    data[sector]['dec']['actual'] += sale.dec
                data['totals']['actual'] += data[sector]['oct']['actual']
                data['totals']['actual'] += data[sector]['nov']['actual']
                data['totals']['actual'] += data[sector]['dec']['actual']
                data['totals']['budget'] += data[sector]['oct']['budget']
                data['totals']['budget'] += data[sector]['nov']['budget']
                data['totals']['budget'] += data[sector]['dec']['budget']
            totals = {
                'oct_actual': 0,
                'oct_budget': 0,
                'nov_actual': 0,
                'nov_budget': 0,
                'dec_actual': 0,
                'dec_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['oct_actual'] += value['oct']['actual']
                    totals['oct_budget'] += value['oct']['budget']
                    totals['nov_actual'] += value['nov']['actual']
                    totals['nov_budget'] += value['nov']['budget']
                    totals['dec_actual'] += value['dec']['actual']
                    totals['dec_budget'] += value['dec']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'sector'
            context['data'] = data
            context['plant'] = plant
            context['totals'] = totals
            context['q'] = 'Q4'
        else:
            pass
        return context

#########################################
########## A VS B REGION PLANT ##########
#########################################

class ChooseLocationVsRegionPlant(ChooseLocationView):
    def get_context_data(self, **kwargs):
        locations = {
            budget.location.region for budget in Budget.objects.all()
        } & {
            sale.location.region for sale in Sale.objects.all()
        }
        context = super().get_context_data(**kwargs)
        context['locations'] = locations
        context['redirect'] = 'cy_vs_region_plant'
        return context

class ChooseYearVsRegionPlant(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {
            budget.year for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'])
        } & {
            sale.year for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'])
        }
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'cq_vs_region_plant'
        return context

class ChooseQuarterVsRegionPlant(ChooseQuarterView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quarters'] = ['q1', 'q2', 'q3', 'q4']
        context['redirect'] = 'vs_region_plant'
        return context

class VsRegionPlant(VersusView):
    def get_context_data(self, **kwargs):
        plants = {
            budget.location for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'])
        } & {
            sale.location for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'])
        }
        if self.kwargs['q'] == 'q1':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for plant in plants:
                data[plant] = {
                    'jan': {
                        'budget': 0,
                        'actual': 0
                    },
                    'feb': {
                        'budget': 0,
                        'actual': 0
                    },
                    'mar': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location=plant):
                    data[plant]['jan']['budget'] += budget.jan
                    data[plant]['feb']['budget'] += budget.feb
                    data[plant]['mar']['budget'] += budget.mar
                for sale in Sale.objects.filter(location=plant):
                    data[plant]['jan']['actual'] += sale.jan
                    data[plant]['feb']['actual'] += sale.feb
                    data[plant]['mar']['actual'] += sale.mar
                data['totals']['actual'] += data[plant]['jan']['actual']
                data['totals']['actual'] += data[plant]['feb']['actual']
                data['totals']['actual'] += data[plant]['mar']['actual']
                data['totals']['budget'] += data[plant]['jan']['budget']
                data['totals']['budget'] += data[plant]['feb']['budget']
                data['totals']['budget'] += data[plant]['mar']['budget']
            totals = {
                'jan_actual': 0,
                'jan_budget': 0,
                'feb_actual': 0,
                'feb_budget': 0,
                'mar_actual': 0,
                'mar_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jan_actual'] += value['jan']['actual']
                    totals['jan_budget'] += value['jan']['budget']
                    totals['feb_actual'] += value['feb']['actual']
                    totals['feb_budget'] += value['feb']['budget']
                    totals['mar_actual'] += value['mar']['actual']
                    totals['mar_budget'] += value['mar']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'plant'
            context['data'] = data
            context['totals'] = totals
            context['region'] = Region.objects.get(slug=self.kwargs['region_name_slug'])
            context['q'] = 'Q1'

        elif self.kwargs['q'] == 'q2':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for plant in plants:
                data[plant] = {
                    'apr': {
                        'budget': 0,
                        'actual': 0
                    },
                    'may': {
                        'budget': 0,
                        'actual': 0
                    },
                    'jun': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location=plant):
                    data[plant]['apr']['budget'] += budget.apr
                    data[plant]['may']['budget'] += budget.may
                    data[plant]['jun']['budget'] += budget.jun
                for sale in Sale.objects.filter(location=plant):
                    data[plant]['apr']['actual'] += sale.apr
                    data[plant]['may']['actual'] += sale.may
                    data[plant]['jun']['actual'] += sale.jun
                data['totals']['actual'] += data[plant]['apr']['actual']
                data['totals']['actual'] += data[plant]['may']['actual']
                data['totals']['actual'] += data[plant]['jun']['actual']
                data['totals']['budget'] += data[plant]['apr']['budget']
                data['totals']['budget'] += data[plant]['may']['budget']
                data['totals']['budget'] += data[plant]['jun']['budget']
            totals = {
                'apr_actual': 0,
                'apr_budget': 0,
                'may_actual': 0,
                'may_budget': 0,
                'jun_actual': 0,
                'jun_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['apr_actual'] += value['apr']['actual']
                    totals['apr_budget'] += value['apr']['budget']
                    totals['may_actual'] += value['may']['actual']
                    totals['may_budget'] += value['may']['budget']
                    totals['jun_actual'] += value['jun']['actual']
                    totals['jun_budget'] += value['jun']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'plant'
            context['data'] = data
            context['totals'] = totals
            context['region'] = Region.objects.get(slug=self.kwargs['region_name_slug'])
            context['q'] = 'Q2'

        elif self.kwargs['q'] == 'q3':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for plant in plants:
                data[plant] = {
                    'jul': {
                        'budget': 0,
                        'actual': 0
                    },
                    'aug': {
                        'budget': 0,
                        'actual': 0
                    },
                    'sep': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location=plant):
                    data[plant]['jul']['budget'] += budget.jul
                    data[plant]['aug']['budget'] += budget.aug
                    data[plant]['sep']['budget'] += budget.sep
                for sale in Sale.objects.filter(location=plant):
                    data[plant]['jul']['actual'] += sale.jul
                    data[plant]['aug']['actual'] += sale.aug
                    data[plant]['sep']['actual'] += sale.sep
                data['totals']['actual'] += data[plant]['jul']['actual']
                data['totals']['actual'] += data[plant]['aug']['actual']
                data['totals']['actual'] += data[plant]['sep']['actual']
                data['totals']['budget'] += data[plant]['jul']['budget']
                data['totals']['budget'] += data[plant]['aug']['budget']
                data['totals']['budget'] += data[plant]['sep']['budget']
            totals = {
                'jul_actual': 0,
                'jul_budget': 0,
                'aug_actual': 0,
                'aug_budget': 0,
                'sep_actual': 0,
                'sep_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jul_actual'] += value['jul']['actual']
                    totals['jul_budget'] += value['jul']['budget']
                    totals['aug_actual'] += value['aug']['actual']
                    totals['aug_budget'] += value['aug']['budget']
                    totals['sep_actual'] += value['sep']['actual']
                    totals['sep_budget'] += value['sep']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'plant'
            context['data'] = data
            context['totals'] = totals
            context['region'] = Region.objects.get(slug=self.kwargs['region_name_slug'])
            context['q'] = 'Q3'

        elif self.kwargs['q'] == 'q4':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for plant in plants:
                data[plant] = {
                    'oct': {
                        'budget': 0,
                        'actual': 0
                    },
                    'nov': {
                        'budget': 0,
                        'actual': 0
                    },
                    'dec': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location=plant):
                    data[plant]['oct']['budget'] += budget.oct
                    data[plant]['nov']['budget'] += budget.nov
                    data[plant]['dec']['budget'] += budget.dec
                for sale in Sale.objects.filter(location=plant):
                    data[plant]['oct']['actual'] += sale.oct
                    data[plant]['nov']['actual'] += sale.nov
                    data[plant]['dec']['actual'] += sale.dec
                data['totals']['actual'] += data[plant]['oct']['actual']
                data['totals']['actual'] += data[plant]['nov']['actual']
                data['totals']['actual'] += data[plant]['dec']['actual']
                data['totals']['budget'] += data[plant]['oct']['budget']
                data['totals']['budget'] += data[plant]['nov']['budget']
                data['totals']['budget'] += data[plant]['dec']['budget']
            totals = {
                'oct_actual': 0,
                'oct_budget': 0,
                'nov_actual': 0,
                'nov_budget': 0,
                'dec_actual': 0,
                'dec_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['oct_actual'] += value['oct']['actual']
                    totals['oct_budget'] += value['oct']['budget']
                    totals['nov_actual'] += value['nov']['actual']
                    totals['nov_budget'] += value['nov']['budget']
                    totals['dec_actual'] += value['dec']['actual']
                    totals['dec_budget'] += value['dec']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'plant'
            context['data'] = data
            context['totals'] = totals
            context['region'] = Region.objects.get(slug=self.kwargs['region_name_slug'])
            context['q'] = 'Q4'
        else:
            pass
        return context

###############################################
########## A VS B REGION BY CUSTOMER ##########
###############################################

class ChooseLocationVsRegionCustomer(ChooseLocationView):
    def get_context_data(self, **kwargs):
        locations = {
            budget.location.region for budget in Budget.objects.all()
        } & {
            sale.location.region for sale in Sale.objects.all()
        }
        context = super().get_context_data(**kwargs)
        context['locations'] = locations
        context['redirect'] = 'cy_vs_region_customer'
        return context

class ChooseYearVsRegionCustomer(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {
            budget.year for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'])
        } & {
            sale.year for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'])
        }
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'cq_vs_region_customer'
        return context

class ChooseQuarterVsRegionCustomer(ChooseQuarterView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quarters'] = ['q1', 'q2', 'q3', 'q4']
        context['redirect'] = 'vs_region_customer'
        return context

class VsRegionCustomer(VersusView):
    def get_context_data(self, **kwargs):
        customers = {
            budget.customer for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'])
        } & {
            sale.customer for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'])
        }
        if self.kwargs['q'] == 'q1':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for customer in customers:
                data[customer] = {
                    'jan': {
                        'budget': 0,
                        'actual': 0
                    },
                    'feb': {
                        'budget': 0,
                        'actual': 0
                    },
                    'mar': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer=customer):
                    data[customer]['jan']['budget'] += budget.jan
                    data[customer]['feb']['budget'] += budget.feb
                    data[customer]['mar']['budget'] += budget.mar
                for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer=customer):
                    data[customer]['jan']['actual'] += sale.jan
                    data[customer]['feb']['actual'] += sale.feb
                    data[customer]['mar']['actual'] += sale.mar
                data['totals']['actual'] += data[customer]['jan']['actual']
                data['totals']['actual'] += data[customer]['feb']['actual']
                data['totals']['actual'] += data[customer]['mar']['actual']
                data['totals']['budget'] += data[customer]['jan']['budget']
                data['totals']['budget'] += data[customer]['feb']['budget']
                data['totals']['budget'] += data[customer]['mar']['budget']
            totals = {
                'jan_actual': 0,
                'jan_budget': 0,
                'feb_actual': 0,
                'feb_budget': 0,
                'mar_actual': 0,
                'mar_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jan_actual'] += value['jan']['actual']
                    totals['jan_budget'] += value['jan']['budget']
                    totals['feb_actual'] += value['feb']['actual']
                    totals['feb_budget'] += value['feb']['budget']
                    totals['mar_actual'] += value['mar']['actual']
                    totals['mar_budget'] += value['mar']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'customer'
            context['data'] = data
            context['totals'] = totals
            context['region'] = Region.objects.get(slug=self.kwargs['region_name_slug'])
            context['q'] = 'Q1'

        elif self.kwargs['q'] == 'q2':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for customer in customers:
                data[customer] = {
                    'apr': {
                        'budget': 0,
                        'actual': 0
                    },
                    'may': {
                        'budget': 0,
                        'actual': 0
                    },
                    'jun': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer=customer):
                    data[customer]['apr']['budget'] += budget.apr
                    data[customer]['may']['budget'] += budget.may
                    data[customer]['jun']['budget'] += budget.jun
                for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer=customer):
                    data[customer]['apr']['actual'] += sale.apr
                    data[customer]['may']['actual'] += sale.may
                    data[customer]['jun']['actual'] += sale.jun
                data['totals']['actual'] += data[customer]['apr']['actual']
                data['totals']['actual'] += data[customer]['may']['actual']
                data['totals']['actual'] += data[customer]['jun']['actual']
                data['totals']['budget'] += data[customer]['apr']['budget']
                data['totals']['budget'] += data[customer]['may']['budget']
                data['totals']['budget'] += data[customer]['jun']['budget']
            totals = {
                'apr_actual': 0,
                'apr_budget': 0,
                'may_actual': 0,
                'may_budget': 0,
                'jun_actual': 0,
                'jun_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['apr_actual'] += value['apr']['actual']
                    totals['apr_budget'] += value['apr']['budget']
                    totals['may_actual'] += value['may']['actual']
                    totals['may_budget'] += value['may']['budget']
                    totals['jun_actual'] += value['jun']['actual']
                    totals['jun_budget'] += value['jun']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'customer'
            context['data'] = data
            context['totals'] = totals
            context['region'] = Region.objects.get(slug=self.kwargs['region_name_slug'])
            context['q'] = 'Q2'

        elif self.kwargs['q'] == 'q3':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for customer in customers:
                data[customer] = {
                    'jul': {
                        'budget': 0,
                        'actual': 0
                    },
                    'aug': {
                        'budget': 0,
                        'actual': 0
                    },
                    'sep': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer=customer):
                    data[customer]['jul']['budget'] += budget.jul
                    data[customer]['aug']['budget'] += budget.aug
                    data[customer]['sep']['budget'] += budget.sep
                for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer=customer):
                    data[customer]['jul']['actual'] += sale.jul
                    data[customer]['aug']['actual'] += sale.aug
                    data[customer]['sep']['actual'] += sale.sep
                data['totals']['actual'] += data[customer]['jul']['actual']
                data['totals']['actual'] += data[customer]['aug']['actual']
                data['totals']['actual'] += data[customer]['sep']['actual']
                data['totals']['budget'] += data[customer]['jul']['budget']
                data['totals']['budget'] += data[customer]['aug']['budget']
                data['totals']['budget'] += data[customer]['sep']['budget']
            totals = {
                'jul_actual': 0,
                'jul_budget': 0,
                'aug_actual': 0,
                'aug_budget': 0,
                'sep_actual': 0,
                'sep_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jul_actual'] += value['jul']['actual']
                    totals['jul_budget'] += value['jul']['budget']
                    totals['aug_actual'] += value['aug']['actual']
                    totals['aug_budget'] += value['aug']['budget']
                    totals['sep_actual'] += value['sep']['actual']
                    totals['sep_budget'] += value['sep']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'customer'
            context['data'] = data
            context['totals'] = totals
            context['region'] = Region.objects.get(slug=self.kwargs['region_name_slug'])
            context['q'] = 'Q3'

        elif self.kwargs['q'] == 'q4':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for customer in customers:
                data[customer] = {
                    'oct': {
                        'budget': 0,
                        'actual': 0
                    },
                    'nov': {
                        'budget': 0,
                        'actual': 0
                    },
                    'dec': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer=customer):
                    data[customer]['oct']['budget'] += budget.oct
                    data[customer]['nov']['budget'] += budget.nov
                    data[customer]['dec']['budget'] += budget.dec
                for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer=customer):
                    data[customer]['oct']['actual'] += sale.oct
                    data[customer]['nov']['actual'] += sale.nov
                    data[customer]['dec']['actual'] += sale.dec
                data['totals']['actual'] += data[customer]['oct']['actual']
                data['totals']['actual'] += data[customer]['nov']['actual']
                data['totals']['actual'] += data[customer]['dec']['actual']
                data['totals']['budget'] += data[customer]['oct']['budget']
                data['totals']['budget'] += data[customer]['nov']['budget']
                data['totals']['budget'] += data[customer]['dec']['budget']
            totals = {
                'oct_actual': 0,
                'oct_budget': 0,
                'nov_actual': 0,
                'nov_budget': 0,
                'dec_actual': 0,
                'dec_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['oct_actual'] += value['oct']['actual']
                    totals['oct_budget'] += value['oct']['budget']
                    totals['nov_actual'] += value['nov']['actual']
                    totals['nov_budget'] += value['nov']['budget']
                    totals['dec_actual'] += value['dec']['actual']
                    totals['dec_budget'] += value['dec']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'customer'
            context['data'] = data
            context['totals'] = totals
            context['region'] = Region.objects.get(slug=self.kwargs['region_name_slug'])
            context['q'] = 'Q4'
        else:
            pass
        return context

##############################################
########## A VS B REGION  BY SECTOR ##########
##############################################

class ChooseLocationVsRegionSector(ChooseLocationView):
    def get_context_data(self, **kwargs):
        locations = {
            budget.location.region for budget in Budget.objects.all()
        } & {
            sale.location.region for sale in Sale.objects.all()
        }
        context = super().get_context_data(**kwargs)
        context['locations'] = locations
        context['redirect'] = 'cy_vs_region_sector'
        return context

class ChooseYearVsRegionSector(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {
            budget.year for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'])
        } & {
            sale.year for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'])
        }
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'cq_vs_region_sector'
        return context

class ChooseQuarterVsRegionSector(ChooseQuarterView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quarters'] = ['q1', 'q2', 'q3', 'q4']
        context['redirect'] = 'vs_region_sector'
        return context

class VsRegionSector(VersusView):
    def get_context_data(self, **kwargs):
        sectors = {
            budget.customer.sector for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'])
        } & {
            sale.customer.sector for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'])
        }
        if self.kwargs['q'] == 'q1':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for sector in sectors:
                data[sector] = {
                    'jan': {
                        'budget': 0,
                        'actual': 0
                    },
                    'feb': {
                        'budget': 0,
                        'actual': 0
                    },
                    'mar': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer__sector=sector):
                    data[sector]['jan']['budget'] += budget.jan
                    data[sector]['feb']['budget'] += budget.feb
                    data[sector]['mar']['budget'] += budget.mar
                for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer__sector=sector):
                    data[sector]['jan']['actual'] += sale.jan
                    data[sector]['feb']['actual'] += sale.feb
                    data[sector]['mar']['actual'] += sale.mar
                data['totals']['actual'] += data[sector]['jan']['actual']
                data['totals']['actual'] += data[sector]['feb']['actual']
                data['totals']['actual'] += data[sector]['mar']['actual']
                data['totals']['budget'] += data[sector]['jan']['budget']
                data['totals']['budget'] += data[sector]['feb']['budget']
                data['totals']['budget'] += data[sector]['mar']['budget']
            totals = {
                'jan_actual': 0,
                'jan_budget': 0,
                'feb_actual': 0,
                'feb_budget': 0,
                'mar_actual': 0,
                'mar_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jan_actual'] += value['jan']['actual']
                    totals['jan_budget'] += value['jan']['budget']
                    totals['feb_actual'] += value['feb']['actual']
                    totals['feb_budget'] += value['feb']['budget']
                    totals['mar_actual'] += value['mar']['actual']
                    totals['mar_budget'] += value['mar']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'sector'
            context['data'] = data
            context['totals'] = totals
            context['region'] = Region.objects.get(slug=self.kwargs['region_name_slug'])
            context['q'] = 'Q1'

        elif self.kwargs['q'] == 'q2':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for sector in sectors:
                data[sector] = {
                    'apr': {
                        'budget': 0,
                        'actual': 0
                    },
                    'may': {
                        'budget': 0,
                        'actual': 0
                    },
                    'jun': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer__sector=sector):
                    data[sector]['apr']['budget'] += budget.apr
                    data[sector]['may']['budget'] += budget.may
                    data[sector]['jun']['budget'] += budget.jun
                for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer__sector=sector):
                    data[sector]['apr']['actual'] += sale.apr
                    data[sector]['may']['actual'] += sale.may
                    data[sector]['jun']['actual'] += sale.jun
                data['totals']['actual'] += data[sector]['apr']['actual']
                data['totals']['actual'] += data[sector]['may']['actual']
                data['totals']['actual'] += data[sector]['jun']['actual']
                data['totals']['budget'] += data[sector]['apr']['budget']
                data['totals']['budget'] += data[sector]['may']['budget']
                data['totals']['budget'] += data[sector]['jun']['budget']
            totals = {
                'apr_actual': 0,
                'apr_budget': 0,
                'may_actual': 0,
                'may_budget': 0,
                'jun_actual': 0,
                'jun_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['apr_actual'] += value['apr']['actual']
                    totals['apr_budget'] += value['apr']['budget']
                    totals['may_actual'] += value['may']['actual']
                    totals['may_budget'] += value['may']['budget']
                    totals['jun_actual'] += value['jun']['actual']
                    totals['jun_budget'] += value['jun']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'sector'
            context['data'] = data
            context['totals'] = totals
            context['region'] = Region.objects.get(slug=self.kwargs['region_name_slug'])
            context['q'] = 'Q2'

        elif self.kwargs['q'] == 'q3':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for sector in sectors:
                data[sector] = {
                    'jul': {
                        'budget': 0,
                        'actual': 0
                    },
                    'aug': {
                        'budget': 0,
                        'actual': 0
                    },
                    'sep': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer__sector=sector):
                    data[sector]['jul']['budget'] += budget.jul
                    data[sector]['aug']['budget'] += budget.aug
                    data[sector]['sep']['budget'] += budget.sep
                for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer__sector=sector):
                    data[sector]['jul']['actual'] += sale.jul
                    data[sector]['aug']['actual'] += sale.aug
                    data[sector]['sep']['actual'] += sale.sep
                data['totals']['actual'] += data[sector]['jul']['actual']
                data['totals']['actual'] += data[sector]['aug']['actual']
                data['totals']['actual'] += data[sector]['sep']['actual']
                data['totals']['budget'] += data[sector]['jul']['budget']
                data['totals']['budget'] += data[sector]['aug']['budget']
                data['totals']['budget'] += data[sector]['sep']['budget']
            totals = {
                'jul_actual': 0,
                'jul_budget': 0,
                'aug_actual': 0,
                'aug_budget': 0,
                'sep_actual': 0,
                'sep_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jul_actual'] += value['jul']['actual']
                    totals['jul_budget'] += value['jul']['budget']
                    totals['aug_actual'] += value['aug']['actual']
                    totals['aug_budget'] += value['aug']['budget']
                    totals['sep_actual'] += value['sep']['actual']
                    totals['sep_budget'] += value['sep']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'sector'
            context['data'] = data
            context['totals'] = totals
            context['region'] = Region.objects.get(slug=self.kwargs['region_name_slug'])
            context['q'] = 'Q3'

        elif self.kwargs['q'] == 'q4':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for sector in sectors:
                data[sector] = {
                    'oct': {
                        'budget': 0,
                        'actual': 0
                    },
                    'nov': {
                        'budget': 0,
                        'actual': 0
                    },
                    'dec': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer__sector=sector):
                    data[sector]['oct']['budget'] += budget.oct
                    data[sector]['nov']['budget'] += budget.nov
                    data[sector]['dec']['budget'] += budget.dec
                for sale in Sale.objects.filter(location__region__slug=self.kwargs['region_name_slug'], customer__sector=sector):
                    data[sector]['oct']['actual'] += sale.oct
                    data[sector]['nov']['actual'] += sale.nov
                    data[sector]['dec']['actual'] += sale.dec
                data['totals']['actual'] += data[sector]['oct']['actual']
                data['totals']['actual'] += data[sector]['nov']['actual']
                data['totals']['actual'] += data[sector]['dec']['actual']
                data['totals']['budget'] += data[sector]['oct']['budget']
                data['totals']['budget'] += data[sector]['nov']['budget']
                data['totals']['budget'] += data[sector]['dec']['budget']
            totals = {
                'oct_actual': 0,
                'oct_budget': 0,
                'nov_actual': 0,
                'nov_budget': 0,
                'dec_actual': 0,
                'dec_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['oct_actual'] += value['oct']['actual']
                    totals['oct_budget'] += value['oct']['budget']
                    totals['nov_actual'] += value['nov']['actual']
                    totals['nov_budget'] += value['nov']['budget']
                    totals['dec_actual'] += value['dec']['actual']
                    totals['dec_budget'] += value['dec']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'sector'
            context['data'] = data
            context['totals'] = totals
            context['region'] = Region.objects.get(slug=self.kwargs['region_name_slug'])
            context['q'] = 'Q4'
        else:
            pass
        return context

############################################
########## A VS B GLOBAL BY PLANT ##########
############################################

class ChooseYearVsGlobalPlant(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {
            budget.year for budget in Budget.objects.all()
        } & {
            sale.year for sale in Sale.objects.all()
        }
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'cq_vs_global_plant'
        return context

class ChooseQuarterVsGlobalPlant(ChooseQuarterView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quarters'] = ['q1', 'q2', 'q3', 'q4']
        context['redirect'] = 'vs_global_plant'
        return context

class VsGlobalPlant(VersusView):
    def get_context_data(self, **kwargs):
        plants = {
            budget.location for budget in Budget.objects.all()
        } & {
            sale.location for sale in Sale.objects.all()
        }
        if self.kwargs['q'] == 'q1':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for plant in plants:
                data[plant] = {
                    'jan': {
                        'budget': 0,
                        'actual': 0
                    },
                    'feb': {
                        'budget': 0,
                        'actual': 0
                    },
                    'mar': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location=plant):
                    data[plant]['jan']['budget'] += budget.jan
                    data[plant]['feb']['budget'] += budget.feb
                    data[plant]['mar']['budget'] += budget.mar
                for sale in Sale.objects.filter(location=plant):
                    data[plant]['jan']['actual'] += sale.jan
                    data[plant]['feb']['actual'] += sale.feb
                    data[plant]['mar']['actual'] += sale.mar
                data['totals']['actual'] += data[plant]['jan']['actual']
                data['totals']['actual'] += data[plant]['feb']['actual']
                data['totals']['actual'] += data[plant]['mar']['actual']
                data['totals']['budget'] += data[plant]['jan']['budget']
                data['totals']['budget'] += data[plant]['feb']['budget']
                data['totals']['budget'] += data[plant]['mar']['budget']
            totals = {
                'jan_actual': 0,
                'jan_budget': 0,
                'feb_actual': 0,
                'feb_budget': 0,
                'mar_actual': 0,
                'mar_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jan_actual'] += value['jan']['actual']
                    totals['jan_budget'] += value['jan']['budget']
                    totals['feb_actual'] += value['feb']['actual']
                    totals['feb_budget'] += value['feb']['budget']
                    totals['mar_actual'] += value['mar']['actual']
                    totals['mar_budget'] += value['mar']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'plant'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q1'

        elif self.kwargs['q'] == 'q2':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for plant in plants:
                data[plant] = {
                    'apr': {
                        'budget': 0,
                        'actual': 0
                    },
                    'may': {
                        'budget': 0,
                        'actual': 0
                    },
                    'jun': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location=plant):
                    data[plant]['apr']['budget'] += budget.apr
                    data[plant]['may']['budget'] += budget.may
                    data[plant]['jun']['budget'] += budget.jun
                for sale in Sale.objects.filter(location=plant):
                    data[plant]['apr']['actual'] += sale.apr
                    data[plant]['may']['actual'] += sale.may
                    data[plant]['jun']['actual'] += sale.jun
                data['totals']['actual'] += data[plant]['apr']['actual']
                data['totals']['actual'] += data[plant]['may']['actual']
                data['totals']['actual'] += data[plant]['jun']['actual']
                data['totals']['budget'] += data[plant]['apr']['budget']
                data['totals']['budget'] += data[plant]['may']['budget']
                data['totals']['budget'] += data[plant]['jun']['budget']
            totals = {
                'apr_actual': 0,
                'apr_budget': 0,
                'may_actual': 0,
                'may_budget': 0,
                'jun_actual': 0,
                'jun_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['apr_actual'] += value['apr']['actual']
                    totals['apr_budget'] += value['apr']['budget']
                    totals['may_actual'] += value['may']['actual']
                    totals['may_budget'] += value['may']['budget']
                    totals['jun_actual'] += value['jun']['actual']
                    totals['jun_budget'] += value['jun']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'plant'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q2'

        elif self.kwargs['q'] == 'q3':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for plant in plants:
                data[plant] = {
                    'jul': {
                        'budget': 0,
                        'actual': 0
                    },
                    'aug': {
                        'budget': 0,
                        'actual': 0
                    },
                    'sep': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location=plant):
                    data[plant]['jul']['budget'] += budget.jul
                    data[plant]['aug']['budget'] += budget.aug
                    data[plant]['sep']['budget'] += budget.sep
                for sale in Sale.objects.filter(location=plant):
                    data[plant]['jul']['actual'] += sale.jul
                    data[plant]['aug']['actual'] += sale.aug
                    data[plant]['sep']['actual'] += sale.sep
                data['totals']['actual'] += data[plant]['jul']['actual']
                data['totals']['actual'] += data[plant]['aug']['actual']
                data['totals']['actual'] += data[plant]['sep']['actual']
                data['totals']['budget'] += data[plant]['jul']['budget']
                data['totals']['budget'] += data[plant]['aug']['budget']
                data['totals']['budget'] += data[plant]['sep']['budget']
            totals = {
                'jul_actual': 0,
                'jul_budget': 0,
                'aug_actual': 0,
                'aug_budget': 0,
                'sep_actual': 0,
                'sep_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jul_actual'] += value['jul']['actual']
                    totals['jul_budget'] += value['jul']['budget']
                    totals['aug_actual'] += value['aug']['actual']
                    totals['aug_budget'] += value['aug']['budget']
                    totals['sep_actual'] += value['sep']['actual']
                    totals['sep_budget'] += value['sep']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'plant'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q3'

        elif self.kwargs['q'] == 'q4':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for plant in plants:
                data[plant] = {
                    'oct': {
                        'budget': 0,
                        'actual': 0
                    },
                    'nov': {
                        'budget': 0,
                        'actual': 0
                    },
                    'dec': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location=plant):
                    data[plant]['oct']['budget'] += budget.oct
                    data[plant]['nov']['budget'] += budget.nov
                    data[plant]['dec']['budget'] += budget.dec
                for sale in Sale.objects.filter(location=plant):
                    data[plant]['oct']['actual'] += sale.oct
                    data[plant]['nov']['actual'] += sale.nov
                    data[plant]['dec']['actual'] += sale.dec
                data['totals']['actual'] += data[plant]['oct']['actual']
                data['totals']['actual'] += data[plant]['nov']['actual']
                data['totals']['actual'] += data[plant]['dec']['actual']
                data['totals']['budget'] += data[plant]['oct']['budget']
                data['totals']['budget'] += data[plant]['nov']['budget']
                data['totals']['budget'] += data[plant]['dec']['budget']
            totals = {
                'oct_actual': 0,
                'oct_budget': 0,
                'nov_actual': 0,
                'nov_budget': 0,
                'dec_actual': 0,
                'dec_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['oct_actual'] += value['oct']['actual']
                    totals['oct_budget'] += value['oct']['budget']
                    totals['nov_actual'] += value['nov']['actual']
                    totals['nov_budget'] += value['nov']['budget']
                    totals['dec_actual'] += value['dec']['actual']
                    totals['dec_budget'] += value['dec']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'plant'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q4'
        else:
            pass
        return context

###############################################
########## A VS B GLOBAL BY CUSTOMER ##########
###############################################

class ChooseYearVsGlobalCustomer(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {
            budget.year for budget in Budget.objects.all()
        } & {
            sale.year for sale in Sale.objects.all()
        }
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'cq_vs_global_customer'
        return context

class ChooseQuarterVsGlobalCustomer(ChooseQuarterView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quarters'] = ['q1', 'q2', 'q3', 'q4']
        context['redirect'] = 'vs_global_customer'
        return context

class VsGlobalCustomer(VersusView):
    def get_context_data(self, **kwargs):
        customers = {
            budget.customer for budget in Budget.objects.all()
        } & {
            sale.customer for sale in Sale.objects.all()
        }
        if self.kwargs['q'] == 'q1':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for customer in customers:
                data[customer] = {
                    'jan': {
                        'budget': 0,
                        'actual': 0
                    },
                    'feb': {
                        'budget': 0,
                        'actual': 0
                    },
                    'mar': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(customer=customer):
                    data[customer]['jan']['budget'] += budget.jan
                    data[customer]['feb']['budget'] += budget.feb
                    data[customer]['mar']['budget'] += budget.mar
                for sale in Sale.objects.filter(customer=customer):
                    data[customer]['jan']['actual'] += sale.jan
                    data[customer]['feb']['actual'] += sale.feb
                    data[customer]['mar']['actual'] += sale.mar
                data['totals']['actual'] += data[customer]['jan']['actual']
                data['totals']['actual'] += data[customer]['feb']['actual']
                data['totals']['actual'] += data[customer]['mar']['actual']
                data['totals']['budget'] += data[customer]['jan']['budget']
                data['totals']['budget'] += data[customer]['feb']['budget']
                data['totals']['budget'] += data[customer]['mar']['budget']
            totals = {
                'jan_actual': 0,
                'jan_budget': 0,
                'feb_actual': 0,
                'feb_budget': 0,
                'mar_actual': 0,
                'mar_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jan_actual'] += value['jan']['actual']
                    totals['jan_budget'] += value['jan']['budget']
                    totals['feb_actual'] += value['feb']['actual']
                    totals['feb_budget'] += value['feb']['budget']
                    totals['mar_actual'] += value['mar']['actual']
                    totals['mar_budget'] += value['mar']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'customer'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q1'

        elif self.kwargs['q'] == 'q2':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for customer in customers:
                data[customer] = {
                    'apr': {
                        'budget': 0,
                        'actual': 0
                    },
                    'may': {
                        'budget': 0,
                        'actual': 0
                    },
                    'jun': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(customer=customer):
                    data[customer]['apr']['budget'] += budget.apr
                    data[customer]['may']['budget'] += budget.may
                    data[customer]['jun']['budget'] += budget.jun
                for sale in Sale.objects.filter(customer=customer):
                    data[customer]['apr']['actual'] += sale.apr
                    data[customer]['may']['actual'] += sale.may
                    data[customer]['jun']['actual'] += sale.jun
                data['totals']['actual'] += data[customer]['apr']['actual']
                data['totals']['actual'] += data[customer]['may']['actual']
                data['totals']['actual'] += data[customer]['jun']['actual']
                data['totals']['budget'] += data[customer]['apr']['budget']
                data['totals']['budget'] += data[customer]['may']['budget']
                data['totals']['budget'] += data[customer]['jun']['budget']
            totals = {
                'apr_actual': 0,
                'apr_budget': 0,
                'may_actual': 0,
                'may_budget': 0,
                'jun_actual': 0,
                'jun_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['apr_actual'] += value['apr']['actual']
                    totals['apr_budget'] += value['apr']['budget']
                    totals['may_actual'] += value['may']['actual']
                    totals['may_budget'] += value['may']['budget']
                    totals['jun_actual'] += value['jun']['actual']
                    totals['jun_budget'] += value['jun']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'customer'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q2'

        elif self.kwargs['q'] == 'q3':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for customer in customers:
                data[customer] = {
                    'jul': {
                        'budget': 0,
                        'actual': 0
                    },
                    'aug': {
                        'budget': 0,
                        'actual': 0
                    },
                    'sep': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(customer=customer):
                    data[customer]['jul']['budget'] += budget.jul
                    data[customer]['aug']['budget'] += budget.aug
                    data[customer]['sep']['budget'] += budget.sep
                for sale in Sale.objects.filter(customer=customer):
                    data[customer]['jul']['actual'] += sale.jul
                    data[customer]['aug']['actual'] += sale.aug
                    data[customer]['sep']['actual'] += sale.sep
                data['totals']['actual'] += data[customer]['jul']['actual']
                data['totals']['actual'] += data[customer]['aug']['actual']
                data['totals']['actual'] += data[customer]['sep']['actual']
                data['totals']['budget'] += data[customer]['jul']['budget']
                data['totals']['budget'] += data[customer]['aug']['budget']
                data['totals']['budget'] += data[customer]['sep']['budget']
            totals = {
                'jul_actual': 0,
                'jul_budget': 0,
                'aug_actual': 0,
                'aug_budget': 0,
                'sep_actual': 0,
                'sep_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jul_actual'] += value['jul']['actual']
                    totals['jul_budget'] += value['jul']['budget']
                    totals['aug_actual'] += value['aug']['actual']
                    totals['aug_budget'] += value['aug']['budget']
                    totals['sep_actual'] += value['sep']['actual']
                    totals['sep_budget'] += value['sep']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'customer'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q3'

        elif self.kwargs['q'] == 'q4':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for customer in customers:
                data[customer] = {
                    'oct': {
                        'budget': 0,
                        'actual': 0
                    },
                    'nov': {
                        'budget': 0,
                        'actual': 0
                    },
                    'dec': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(customer=customer):
                    data[customer]['oct']['budget'] += budget.oct
                    data[customer]['nov']['budget'] += budget.nov
                    data[customer]['dec']['budget'] += budget.dec
                for sale in Sale.objects.filter(customer=customer):
                    data[customer]['oct']['actual'] += sale.oct
                    data[customer]['nov']['actual'] += sale.nov
                    data[customer]['dec']['actual'] += sale.dec
                data['totals']['actual'] += data[customer]['oct']['actual']
                data['totals']['actual'] += data[customer]['nov']['actual']
                data['totals']['actual'] += data[customer]['dec']['actual']
                data['totals']['budget'] += data[customer]['oct']['budget']
                data['totals']['budget'] += data[customer]['nov']['budget']
                data['totals']['budget'] += data[customer]['dec']['budget']
            totals = {
                'oct_actual': 0,
                'oct_budget': 0,
                'nov_actual': 0,
                'nov_budget': 0,
                'dec_actual': 0,
                'dec_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['oct_actual'] += value['oct']['actual']
                    totals['oct_budget'] += value['oct']['budget']
                    totals['nov_actual'] += value['nov']['actual']
                    totals['nov_budget'] += value['nov']['budget']
                    totals['dec_actual'] += value['dec']['actual']
                    totals['dec_budget'] += value['dec']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'customer'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q4'
        else:
            pass
        return context

###############################################
########## A VS B GLOBAL BY SECTOR ##########
###############################################

class ChooseYearVsGlobalSector(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {
            budget.year for budget in Budget.objects.all()
        } & {
            sale.year for sale in Sale.objects.all()
        }
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'cq_vs_global_sector'
        return context

class ChooseQuarterVsGlobalSector(ChooseQuarterView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quarters'] = ['q1', 'q2', 'q3', 'q4']
        context['redirect'] = 'vs_global_sector'
        return context

class VsGlobalSector(VersusView):
    def get_context_data(self, **kwargs):
        sectors = {
            budget.customer.sector for budget in Budget.objects.all()
        } & {
            sale.customer.sector for sale in Sale.objects.all()
        }
        if self.kwargs['q'] == 'q1':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for sector in sectors:
                data[sector] = {
                    'jan': {
                        'budget': 0,
                        'actual': 0
                    },
                    'feb': {
                        'budget': 0,
                        'actual': 0
                    },
                    'mar': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(customer__sector=sector):
                    data[sector]['jan']['budget'] += budget.jan
                    data[sector]['feb']['budget'] += budget.feb
                    data[sector]['mar']['budget'] += budget.mar
                for sale in Sale.objects.filter(customer__sector=sector):
                    data[sector]['jan']['actual'] += sale.jan
                    data[sector]['feb']['actual'] += sale.feb
                    data[sector]['mar']['actual'] += sale.mar
                data['totals']['actual'] += data[sector]['jan']['actual']
                data['totals']['actual'] += data[sector]['feb']['actual']
                data['totals']['actual'] += data[sector]['mar']['actual']
                data['totals']['budget'] += data[sector]['jan']['budget']
                data['totals']['budget'] += data[sector]['feb']['budget']
                data['totals']['budget'] += data[sector]['mar']['budget']
            totals = {
                'jan_actual': 0,
                'jan_budget': 0,
                'feb_actual': 0,
                'feb_budget': 0,
                'mar_actual': 0,
                'mar_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jan_actual'] += value['jan']['actual']
                    totals['jan_budget'] += value['jan']['budget']
                    totals['feb_actual'] += value['feb']['actual']
                    totals['feb_budget'] += value['feb']['budget']
                    totals['mar_actual'] += value['mar']['actual']
                    totals['mar_budget'] += value['mar']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'sector'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q1'

        elif self.kwargs['q'] == 'q2':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for sector in sectors:
                data[sector] = {
                    'apr': {
                        'budget': 0,
                        'actual': 0
                    },
                    'may': {
                        'budget': 0,
                        'actual': 0
                    },
                    'jun': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(customer__sector=sector):
                    data[sector]['apr']['budget'] += budget.apr
                    data[sector]['may']['budget'] += budget.may
                    data[sector]['jun']['budget'] += budget.jun
                for sale in Sale.objects.filter(customer__sector=sector):
                    data[sector]['apr']['actual'] += sale.apr
                    data[sector]['may']['actual'] += sale.may
                    data[sector]['jun']['actual'] += sale.jun
                data['totals']['actual'] += data[sector]['apr']['actual']
                data['totals']['actual'] += data[sector]['may']['actual']
                data['totals']['actual'] += data[sector]['jun']['actual']
                data['totals']['budget'] += data[sector]['apr']['budget']
                data['totals']['budget'] += data[sector]['may']['budget']
                data['totals']['budget'] += data[sector]['jun']['budget']
            totals = {
                'apr_actual': 0,
                'apr_budget': 0,
                'may_actual': 0,
                'may_budget': 0,
                'jun_actual': 0,
                'jun_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['apr_actual'] += value['apr']['actual']
                    totals['apr_budget'] += value['apr']['budget']
                    totals['may_actual'] += value['may']['actual']
                    totals['may_budget'] += value['may']['budget']
                    totals['jun_actual'] += value['jun']['actual']
                    totals['jun_budget'] += value['jun']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'sector'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q2'

        elif self.kwargs['q'] == 'q3':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for sector in sectors:
                data[sector] = {
                    'jul': {
                        'budget': 0,
                        'actual': 0
                    },
                    'aug': {
                        'budget': 0,
                        'actual': 0
                    },
                    'sep': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(customer__sector=sector):
                    data[sector]['jul']['budget'] += budget.jul
                    data[sector]['aug']['budget'] += budget.aug
                    data[sector]['sep']['budget'] += budget.sep
                for sale in Sale.objects.filter(customer__sector=sector):
                    data[sector]['jul']['actual'] += sale.jul
                    data[sector]['aug']['actual'] += sale.aug
                    data[sector]['sep']['actual'] += sale.sep
                data['totals']['actual'] += data[sector]['jul']['actual']
                data['totals']['actual'] += data[sector]['aug']['actual']
                data['totals']['actual'] += data[sector]['sep']['actual']
                data['totals']['budget'] += data[sector]['jul']['budget']
                data['totals']['budget'] += data[sector]['aug']['budget']
                data['totals']['budget'] += data[sector]['sep']['budget']
            totals = {
                'jul_actual': 0,
                'jul_budget': 0,
                'aug_actual': 0,
                'aug_budget': 0,
                'sep_actual': 0,
                'sep_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jul_actual'] += value['jul']['actual']
                    totals['jul_budget'] += value['jul']['budget']
                    totals['aug_actual'] += value['aug']['actual']
                    totals['aug_budget'] += value['aug']['budget']
                    totals['sep_actual'] += value['sep']['actual']
                    totals['sep_budget'] += value['sep']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'sector'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q3'

        elif self.kwargs['q'] == 'q4':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for sector in sectors:
                data[sector] = {
                    'oct': {
                        'budget': 0,
                        'actual': 0
                    },
                    'nov': {
                        'budget': 0,
                        'actual': 0
                    },
                    'dec': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(customer__sector=sector):
                    data[sector]['oct']['budget'] += budget.oct
                    data[sector]['nov']['budget'] += budget.nov
                    data[sector]['dec']['budget'] += budget.dec
                for sale in Sale.objects.filter(customer__sector=sector):
                    data[sector]['oct']['actual'] += sale.oct
                    data[sector]['nov']['actual'] += sale.nov
                    data[sector]['dec']['actual'] += sale.dec
                data['totals']['actual'] += data[sector]['oct']['actual']
                data['totals']['actual'] += data[sector]['nov']['actual']
                data['totals']['actual'] += data[sector]['dec']['actual']
                data['totals']['budget'] += data[sector]['oct']['budget']
                data['totals']['budget'] += data[sector]['nov']['budget']
                data['totals']['budget'] += data[sector]['dec']['budget']
            totals = {
                'oct_actual': 0,
                'oct_budget': 0,
                'nov_actual': 0,
                'nov_budget': 0,
                'dec_actual': 0,
                'dec_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['oct_actual'] += value['oct']['actual']
                    totals['oct_budget'] += value['oct']['budget']
                    totals['nov_actual'] += value['nov']['actual']
                    totals['nov_budget'] += value['nov']['budget']
                    totals['dec_actual'] += value['dec']['actual']
                    totals['dec_budget'] += value['dec']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'sector'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q4'
        else:
            pass
        return context

###############################################
########## A VS B GLOBAL BY REGION ##########
###############################################

class ChooseYearVsGlobalRegion(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {
            budget.year for budget in Budget.objects.all()
        } & {
            sale.year for sale in Sale.objects.all()
        }
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'cq_vs_global_region'
        return context

class ChooseQuarterVsGlobalRegion(ChooseQuarterView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quarters'] = ['q1', 'q2', 'q3', 'q4']
        context['redirect'] = 'vs_global_region'
        return context

class VsGlobalRegion(VersusView):
    def get_context_data(self, **kwargs):
        regions = {
            budget.location.region for budget in Budget.objects.all()
        } & {
            sale.location.region for sale in Sale.objects.all()
        }
        if self.kwargs['q'] == 'q1':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for region in regions:
                data[region] = {
                    'jan': {
                        'budget': 0,
                        'actual': 0
                    },
                    'feb': {
                        'budget': 0,
                        'actual': 0
                    },
                    'mar': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location__region=region):
                    data[region]['jan']['budget'] += budget.jan
                    data[region]['feb']['budget'] += budget.feb
                    data[region]['mar']['budget'] += budget.mar
                for sale in Sale.objects.filter(location__region=region):
                    data[region]['jan']['actual'] += sale.jan
                    data[region]['feb']['actual'] += sale.feb
                    data[region]['mar']['actual'] += sale.mar
                data['totals']['actual'] += data[region]['jan']['actual']
                data['totals']['actual'] += data[region]['feb']['actual']
                data['totals']['actual'] += data[region]['mar']['actual']
                data['totals']['budget'] += data[region]['jan']['budget']
                data['totals']['budget'] += data[region]['feb']['budget']
                data['totals']['budget'] += data[region]['mar']['budget']
            totals = {
                'jan_actual': 0,
                'jan_budget': 0,
                'feb_actual': 0,
                'feb_budget': 0,
                'mar_actual': 0,
                'mar_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jan_actual'] += value['jan']['actual']
                    totals['jan_budget'] += value['jan']['budget']
                    totals['feb_actual'] += value['feb']['actual']
                    totals['feb_budget'] += value['feb']['budget']
                    totals['mar_actual'] += value['mar']['actual']
                    totals['mar_budget'] += value['mar']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'region'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q1'

        elif self.kwargs['q'] == 'q2':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for region in regions:
                data[region] = {
                    'apr': {
                        'budget': 0,
                        'actual': 0
                    },
                    'may': {
                        'budget': 0,
                        'actual': 0
                    },
                    'jun': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location__region=region):
                    data[region]['apr']['budget'] += budget.apr
                    data[region]['may']['budget'] += budget.may
                    data[region]['jun']['budget'] += budget.jun
                for sale in Sale.objects.filter(location__region=region):
                    data[region]['apr']['actual'] += sale.apr
                    data[region]['may']['actual'] += sale.may
                    data[region]['jun']['actual'] += sale.jun
                data['totals']['actual'] += data[region]['apr']['actual']
                data['totals']['actual'] += data[region]['may']['actual']
                data['totals']['actual'] += data[region]['jun']['actual']
                data['totals']['budget'] += data[region]['apr']['budget']
                data['totals']['budget'] += data[region]['may']['budget']
                data['totals']['budget'] += data[region]['jun']['budget']
            totals = {
                'apr_actual': 0,
                'apr_budget': 0,
                'may_actual': 0,
                'may_budget': 0,
                'jun_actual': 0,
                'jun_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['apr_actual'] += value['apr']['actual']
                    totals['apr_budget'] += value['apr']['budget']
                    totals['may_actual'] += value['may']['actual']
                    totals['may_budget'] += value['may']['budget']
                    totals['jun_actual'] += value['jun']['actual']
                    totals['jun_budget'] += value['jun']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'region'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q2'

        elif self.kwargs['q'] == 'q3':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for region in regions:
                data[region] = {
                    'jul': {
                        'budget': 0,
                        'actual': 0
                    },
                    'aug': {
                        'budget': 0,
                        'actual': 0
                    },
                    'sep': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location__region=region):
                    data[region]['jul']['budget'] += budget.jul
                    data[region]['aug']['budget'] += budget.aug
                    data[region]['sep']['budget'] += budget.sep
                for sale in Sale.objects.filter(location__region=region):
                    data[region]['jul']['actual'] += sale.jul
                    data[region]['aug']['actual'] += sale.aug
                    data[region]['sep']['actual'] += sale.sep
                data['totals']['actual'] += data[region]['jul']['actual']
                data['totals']['actual'] += data[region]['aug']['actual']
                data['totals']['actual'] += data[region]['sep']['actual']
                data['totals']['budget'] += data[region]['jul']['budget']
                data['totals']['budget'] += data[region]['aug']['budget']
                data['totals']['budget'] += data[region]['sep']['budget']
            totals = {
                'jul_actual': 0,
                'jul_budget': 0,
                'aug_actual': 0,
                'aug_budget': 0,
                'sep_actual': 0,
                'sep_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['jul_actual'] += value['jul']['actual']
                    totals['jul_budget'] += value['jul']['budget']
                    totals['aug_actual'] += value['aug']['actual']
                    totals['aug_budget'] += value['aug']['budget']
                    totals['sep_actual'] += value['sep']['actual']
                    totals['sep_budget'] += value['sep']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'region'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q3'

        elif self.kwargs['q'] == 'q4':
            data = {
                'totals': {
                    'actual': 0,
                    'budget': 0
                }
            }
            for region in regions:
                data[region] = {
                    'oct': {
                        'budget': 0,
                        'actual': 0
                    },
                    'nov': {
                        'budget': 0,
                        'actual': 0
                    },
                    'dec': {
                        'budget': 0,
                        'actual': 0
                    },
                }
                for budget in Budget.objects.filter(location__region=region):
                    data[region]['oct']['budget'] += budget.oct
                    data[region]['nov']['budget'] += budget.nov
                    data[region]['dec']['budget'] += budget.dec
                for sale in Sale.objects.filter(location__region=region):
                    data[region]['oct']['actual'] += sale.oct
                    data[region]['nov']['actual'] += sale.nov
                    data[region]['dec']['actual'] += sale.dec
                data['totals']['actual'] += data[region]['oct']['actual']
                data['totals']['actual'] += data[region]['nov']['actual']
                data['totals']['actual'] += data[region]['dec']['actual']
                data['totals']['budget'] += data[region]['oct']['budget']
                data['totals']['budget'] += data[region]['nov']['budget']
                data['totals']['budget'] += data[region]['dec']['budget']
            totals = {
                'oct_actual': 0,
                'oct_budget': 0,
                'nov_actual': 0,
                'nov_budget': 0,
                'dec_actual': 0,
                'dec_budget': 0,
                'total_actual': 0,
                'total_budget': 0
            }
            for key, value in data.items():
                if key != 'totals':
                    totals['oct_actual'] += value['oct']['actual']
                    totals['oct_budget'] += value['oct']['budget']
                    totals['nov_actual'] += value['nov']['actual']
                    totals['nov_budget'] += value['nov']['budget']
                    totals['dec_actual'] += value['dec']['actual']
                    totals['dec_budget'] += value['dec']['budget']
            totals['total_actual'] = data['totals']['actual']
            totals['total_budget'] = data['totals']['budget']
            context = super().get_context_data(**kwargs)
            context['first_col'] = 'region'
            context['data'] = data
            context['totals'] = totals
            context['global'] = True
            context['q'] = 'Q4'
        else:
            pass
        return context