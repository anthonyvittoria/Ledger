from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from .models import Budget, Customer, Sale, Location
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
        context['object_list'] = customers
        return context

class ChooseYearBudgetCustomerPlant(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {budget.year for budget in Budget.objects.filter(
            customer__slug=self.kwargs['customer_name_slug']).order_by('year')}
        context = super().get_context_data(**kwargs)
        context['redirect'] = 'budget_customer_plant'
        context['location_name_slug'] = self.kwargs['customer_name_slug']
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
        context['redirect'] = 'budget_form'
        return context

@login_required
def form_budget(request, location_name_slug):
    location = Location.objects.get(slug=location_name_slug)
    BudgetInlineFormSet = inlineformset_factory(Location, Budget, fields=(
        'customer', 'jan', 'feb',
        'mar', 'apr', 'may', 'jun',
        'jul', 'aug', 'sep', 'oct',
        'nov', 'dec', 'year',
    ), extra=1, min_num=1)
    if request.method == 'POST':
        formset = BudgetInlineFormSet(request.POST, instance=location)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Budget updated successfully.")
            return HttpResponseRedirect('')
    else:
        formset = BudgetInlineFormSet(instance=location)
    return render(request, 'Ledger/budget_form2.html', {'formset': formset, 'location': location})

###########################################
########## A VS B CUSTOMER PLANT ##########
###########################################

class ChooseCustomerVsCustomerPlant(ChooseCustomerView):
    def get_context_data(self, **kwargs):
        # b_customers = [budget.customer.id for budget in Budget.objects.all()]
        # c_customers = [sale.customer.id for sale in Sale.objects.all()]
        # inter = intersection(b_customers, c_customers)
        customers = {
            budget.customer for budget in Budget.objects.all()
        } & {
            sale.customer for sale in Sale.objects.all()
        }
        context = super().get_context_data(**kwargs)
        context['redirect'] = 'cy_vs_customer_plant'
        context['customers'] = customers
        return context

class ChooseYearVsCustomerPlant(ChooseYearView):
    def get_context_data(self, **kwargs):
        years = {
            sale.year for sale in Sale.objects.filter(customer__slug=self.kwargs['customer_name_slug'])
        } & {
            budget.year for budget in Budget.objects.filter(customer__slug=self.kwargs['customer_name_slug'])
        }
        context = super().get_context_data(**kwargs)
        context['years'] = years
        context['redirect'] = 'cq_vs_customer_plant'
        return context

class ChooseQuarterVsCustomerPlant(ChooseQuarterView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ['q1', 'q2', 'q3', 'q4']
        context['redirect'] = 'vs_customer_plant'
        return context

class VsCustomerPlant(VersusView):
    def get_context_data(self, **kwargs):
        customer = Customer.objects.get(slug=self.kwargs['customer_name_slug'])
        if self.kwargs['q'] == 'Q1':
            data = {'budgets': {}, 'actuals': {}}
            for budget in Budget.objects.filter(customer=customer):
                data['budgets']['jan'] += budget.jan
                data['budgets']['feb'] += budget.feb
                data['budgets']['mar'] += budget.mar
            for sale in Sale.objects.filter(customer=customer):
                data['actuals']['jan'] += sale.jan
                data['actuals']['feb'] += sale.feb
                data['actuals']['mar'] += sale.mar
            context = super().get_context_data(**kwargs)
            context['data'] = data
            context['customer'] = customer
            
        elif self.kwargs['q'] == 'Q2':
            months = ['apr', 'may', 'jun']
        elif self.kwargs['q'] == 'Q3':
            months = ['jul', 'aug', 'sep']
        else:
            months = ['oct', 'nov', 'dec']
        context = super().get_context_data(**kwargs)
        context['months'] = months
        context['first_col'] = 'customer'
        return context