from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory

from .models import Budget, Customer, Sale, Location

def index(request):
    return render(request, 'Ledger/index.html')

#################################################
########## BUDGET BY CUSTOMER BY PLANT ##########
#################################################

def cc_budget_customer_plant(request): #Choose customer
    customers = []
    for budget in Budget.objects.all():
        if budget.customer not in customers:
            customers.append(budget.customer)

    context = {
        'customers': customers,
        'redirect': 'cy_budget_customer_plant',
    }
    return render(request, 'Ledger/choose_customer.html', context)

def cy_budget_customer_plant(request, customer_name_slug):

    years = []

    for budget in Budget.objects.filter(customer__slug=customer_name_slug).order_by('year'):
        if budget.year not in years:
            years.append(budget.year)

    context = {
        'years': years,
        'location_name_slug': customer_name_slug,
        'redirect': 'budget_customer_plant',
    }
    return render(request, 'Ledger/choose_year.html', context)

def budget_customer_plant(request, customer_name_slug, year):
    
    budget_objects = Budget.objects.filter(customer__slug=customer_name_slug, year=year)

    plant_data = {}
    for budget in budget_objects:
        if budget.location not in plant_data.keys():
            plant_data[budget.location] = {
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
            plant_data[budget.location]['jan'] += budget.jan
            plant_data[budget.location]['feb'] += budget.feb
            plant_data[budget.location]['mar'] += budget.mar
            plant_data[budget.location]['apr'] += budget.apr
            plant_data[budget.location]['may'] += budget.may
            plant_data[budget.location]['jun'] += budget.jun
            plant_data[budget.location]['jul'] += budget.jul
            plant_data[budget.location]['aug'] += budget.aug
            plant_data[budget.location]['sep'] += budget.sep
            plant_data[budget.location]['oct'] += budget.oct
            plant_data[budget.location]['nov'] += budget.nov
            plant_data[budget.location]['dec'] += budget.dec
            plant_data[budget.location]['q1'] += budget.q1
            plant_data[budget.location]['q2'] += budget.q2
            plant_data[budget.location]['q3'] += budget.q3
            plant_data[budget.location]['q4'] += budget.q4

    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    budget_total = 0

    for plant in plant_data:
        jan_total += plant_data[plant]['jan']
        feb_total += plant_data[plant]['feb']
        mar_total += plant_data[plant]['mar']
        apr_total += plant_data[plant]['apr']
        may_total += plant_data[plant]['may']
        jun_total += plant_data[plant]['jun']
        jul_total += plant_data[plant]['jul']
        aug_total += plant_data[plant]['aug']
        sep_total += plant_data[plant]['sep']
        oct_total += plant_data[plant]['oct']
        nov_total += plant_data[plant]['nov']
        dec_total += plant_data[plant]['dec']
        q1_total += plant_data[plant]['q1']
        q2_total += plant_data[plant]['q2']
        q3_total += plant_data[plant]['q3']
        q4_total += plant_data[plant]['q4']
        budget_total += (plant_data[plant]['q1'] + plant_data[plant]['q2'] + plant_data[plant]['q3'] + plant_data[plant]['q4'])

    context = {
    'budget_data': plant_data,
    'first_col': 'plant',
    'customer': Customer.objects.get(slug=customer_name_slug),
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'budget_total': budget_total,
    }
    return render(request, 'Ledger/budget.html', context)


#################################################
########## BUDGET BY PLANT BY CUSTOMER ##########
#################################################

def cl_budget_plant_customer(request): # Choose location

    # create unique list of plant locations that have budgets recorded for them
    budget_locations = []
    for budget in Budget.objects.all().order_by('location__name'):
        if budget.location not in budget_locations:
            budget_locations.append(budget.location)

    context = {
        'locations': budget_locations,
        'redirect': 'cy_budget_plant_customer',
    }
    return render(request, 'Ledger/choose_location.html', context)

def cy_budget_plant_customer(request, location_name_slug): # Choose year for budget by plant by customer
    
    years = []

    for budget in Budget.objects.filter(location__slug=location_name_slug).order_by('year'):
        if budget.year not in years:
            years.append(budget.year)

    context = {
        'years': years,
        'location_name_slug': location_name_slug,
        'redirect': 'budget_plant_customer',
    }
    return render(request, 'Ledger/choose_year.html', context)

def budget_plant_customer(request, location_name_slug, year): # Budget table view

    budget_objects = Budget.objects.filter(location__slug=location_name_slug, year=year).order_by('customer__name')

    location = budget_objects[0].location
    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    budget_total = 0

    for budget in budget_objects:
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
    
    context = {
        'budget_objects': budget_objects,
        'first_col': 'customer',
        'second_col': 'sector',
        'location': location,
        'year': year,
        'jan_total': jan_total,
        'feb_total': feb_total,
        'mar_total': mar_total,
        'apr_total': apr_total,
        'may_total': may_total,
        'jun_total': jun_total,
        'jul_total': jul_total,
        'aug_total': aug_total,
        'sep_total': sep_total,
        'oct_total': oct_total,
        'nov_total': nov_total,
        'dec_total': dec_total,
        'q1_total': q1_total,
        'q2_total': q2_total,
        'q3_total': q3_total,
        'q4_total': q4_total,
        'budget_total': budget_total,
    }
    return render(request, 'Ledger/budget.html', context)

###############################################
########## BUDGET BY PLANT BY SECTOR ##########
###############################################

def cl_budget_plant_sector(request): # Choose location

    budget_locations = []

    # create unique list of plant locations that have budgets recorded for them
    for budget in Budget.objects.all().order_by('location__name'):
        if budget.location not in budget_locations:
            budget_locations.append(budget.location)

    context = {
        'locations': budget_locations,
        'redirect': 'cy_budget_plant_sector',
    }
    return render(request, 'Ledger/choose_location.html', context)

def cy_budget_plant_sector(request, location_name_slug): # Choose year
    
    years = []

    for budget in Budget.objects.filter(location__slug=location_name_slug).order_by('year'):
        if budget.year not in years:
            years.append(budget.year)

    context = {
        'years': years,
        'location_name_slug': location_name_slug,
        'redirect': 'budget_plant_sector',
    }
    return render(request, 'Ledger/choose_year.html', context)

def budget_plant_sector(request, location_name_slug, year): # Budget table view

    # list of budgets corresponding to this plant and year
    budget_objects = Budget.objects.filter(location__slug=location_name_slug, year=year).order_by('customer__sector')
    
    sector_data = {} # create dictionary of data for each sector
    for budget in budget_objects:
        if budget.customer.sector not in sector_data.keys():
            sector_data[budget.customer.sector] = {
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
            sector_data[budget.customer.sector]['jan'] += budget.jan
            sector_data[budget.customer.sector]['feb'] += budget.feb
            sector_data[budget.customer.sector]['mar'] += budget.mar
            sector_data[budget.customer.sector]['apr'] += budget.apr
            sector_data[budget.customer.sector]['may'] += budget.may
            sector_data[budget.customer.sector]['jun'] += budget.jun
            sector_data[budget.customer.sector]['jul'] += budget.jul
            sector_data[budget.customer.sector]['aug'] += budget.aug
            sector_data[budget.customer.sector]['sep'] += budget.sep
            sector_data[budget.customer.sector]['oct'] += budget.oct
            sector_data[budget.customer.sector]['nov'] += budget.nov
            sector_data[budget.customer.sector]['dec'] += budget.dec
            sector_data[budget.customer.sector]['q1'] += budget.q1
            sector_data[budget.customer.sector]['q2'] += budget.q2
            sector_data[budget.customer.sector]['q3'] += budget.q3
            sector_data[budget.customer.sector]['q4'] += budget.q4

    location = budget_objects[0].location
    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    budget_total = 0

    for sector in sector_data:
        jan_total += sector_data[sector]['jan']
        feb_total += sector_data[sector]['feb']
        mar_total += sector_data[sector]['mar']
        apr_total += sector_data[sector]['apr']
        may_total += sector_data[sector]['may']
        jun_total += sector_data[sector]['jun']
        jul_total += sector_data[sector]['jul']
        aug_total += sector_data[sector]['aug']
        sep_total += sector_data[sector]['sep']
        oct_total += sector_data[sector]['oct']
        nov_total += sector_data[sector]['nov']
        dec_total += sector_data[sector]['dec']
        q1_total += sector_data[sector]['q1']
        q2_total += sector_data[sector]['q2']
        q3_total += sector_data[sector]['q3']
        q4_total += sector_data[sector]['q4']
        budget_total += (sector_data[sector]['q1'] + sector_data[sector]['q2'] + sector_data[sector]['q3'] + sector_data[sector]['q4'])
    
    context = {
    'budget_data': sector_data,
    'first_col': 'sector',
    'location': location,
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'budget_total': budget_total,
    }
    return render(request, 'Ledger/budget.html', context)

###############################################
########## BUDGET BY REGION BY PLANT ##########
###############################################

def cl_budget_region_plant(request): # Choose location
    
    regions = []
    for budget in Budget.objects.all().order_by('location__name'):
        if budget.location.region not in regions:
            regions.append(budget.location.region)
    
    context = {
        'locations': regions,
        'redirect': 'cy_budget_region_plant',
    }
    return render(request, 'Ledger/choose_location.html', context)

def cy_budget_region_plant(request, region_name_slug): # Choose year
    
    years = []

    for budget in Budget.objects.filter(location__region__slug=region_name_slug).order_by('year'):
        if budget.year not in years:
            years.append(budget.year)
    
    context = {
        'years': years,
        'location_name_slug': region_name_slug,
        'redirect': 'budget_region_plant',
    }
    return render(request, 'Ledger/choose_year.html', context)

def budget_region_plant(request, region_name_slug, year): # Budget table view

    # list of budgets corresponding to this region and year
    budget_objects = Budget.objects.filter(location__region__slug=region_name_slug, year=year).order_by('location__name')

    plant_data = {} # create dictionary of data for each plant
    for budget in budget_objects:
        if budget.location not in plant_data.keys():
            plant_data[budget.location] = {
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
            plant_data[budget.location]['jan'] += budget.jan
            plant_data[budget.location]['feb'] += budget.feb
            plant_data[budget.location]['mar'] += budget.mar
            plant_data[budget.location]['apr'] += budget.apr
            plant_data[budget.location]['may'] += budget.may
            plant_data[budget.location]['jun'] += budget.jun
            plant_data[budget.location]['jul'] += budget.jul
            plant_data[budget.location]['aug'] += budget.aug
            plant_data[budget.location]['sep'] += budget.sep
            plant_data[budget.location]['oct'] += budget.oct
            plant_data[budget.location]['nov'] += budget.nov
            plant_data[budget.location]['dec'] += budget.dec
            plant_data[budget.location]['q1'] += budget.q1
            plant_data[budget.location]['q2'] += budget.q2
            plant_data[budget.location]['q3'] += budget.q3
            plant_data[budget.location]['q4'] += budget.q4

    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    budget_total = 0

    for plant in plant_data:
        jan_total += plant_data[plant]['jan']
        feb_total += plant_data[plant]['feb']
        mar_total += plant_data[plant]['mar']
        apr_total += plant_data[plant]['apr']
        may_total += plant_data[plant]['may']
        jun_total += plant_data[plant]['jun']
        jul_total += plant_data[plant]['jul']
        aug_total += plant_data[plant]['aug']
        sep_total += plant_data[plant]['sep']
        oct_total += plant_data[plant]['oct']
        nov_total += plant_data[plant]['nov']
        dec_total += plant_data[plant]['dec']
        q1_total += plant_data[plant]['q1']
        q2_total += plant_data[plant]['q2']
        q3_total += plant_data[plant]['q3']
        q4_total += plant_data[plant]['q4']
        budget_total += (plant_data[plant]['q1'] + plant_data[plant]['q2'] + plant_data[plant]['q3'] + plant_data[plant]['q4'])

    context = {
        'budget_data': plant_data,
        'first_col': 'plant',
        'region': budget_objects[0].location.region,
        'year': year,
        'jan_total': jan_total,
        'feb_total': feb_total,
        'mar_total': mar_total,
        'apr_total': apr_total,
        'may_total': may_total,
        'jun_total': jun_total,
        'jul_total': jul_total,
        'aug_total': aug_total,
        'sep_total': sep_total,
        'oct_total': oct_total,
        'nov_total': nov_total,
        'dec_total': dec_total,
        'q1_total': q1_total,
        'q2_total': q2_total,
        'q3_total': q3_total,
        'q4_total': q4_total,
        'budget_total': budget_total,
    }
    return render(request, 'Ledger/budget.html', context)

##################################################
########## BUDGET BY REGION BY CUSTOMER ##########
##################################################

def cl_budget_region_customer(request): # Choose location
    regions = []
    for budget in Budget.objects.all().order_by('location__name'):
        if budget.location.region not in regions:
            regions.append(budget.location.region)
    
    context = {
        'locations': regions,
        'redirect': 'cy_budget_region_customer',
    }
    return render(request, 'Ledger/choose_location.html', context)

def cy_budget_region_customer(request, region_name_slug): # Choose year

    years = []

    for budget in Budget.objects.filter(location__region__slug=region_name_slug).order_by('year'):
        if budget.year not in years:
            years.append(budget.year)
    
    context = {
        'years': years,
        'location_name_slug': region_name_slug,
        'redirect': 'budget_region_customer',
    }
    return render(request, 'Ledger/choose_year.html', context)

def budget_region_customer(request, region_name_slug, year):

    
    # list of budgets corresponding to this region and year
    budget_objects = Budget.objects.filter(location__region__slug=region_name_slug, year=year).order_by('customer__name')

    customer_data = {} # create dictionary of data for each customer
    for budget in budget_objects:
        if budget.customer not in customer_data.keys():
            customer_data[budget.customer] = {
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
            customer_data[budget.customer]['jan'] += budget.jan
            customer_data[budget.customer]['feb'] += budget.feb
            customer_data[budget.customer]['mar'] += budget.mar
            customer_data[budget.customer]['apr'] += budget.apr
            customer_data[budget.customer]['may'] += budget.may
            customer_data[budget.customer]['jun'] += budget.jun
            customer_data[budget.customer]['jul'] += budget.jul
            customer_data[budget.customer]['aug'] += budget.aug
            customer_data[budget.customer]['sep'] += budget.sep
            customer_data[budget.customer]['oct'] += budget.oct
            customer_data[budget.customer]['nov'] += budget.nov
            customer_data[budget.customer]['dec'] += budget.dec
            customer_data[budget.customer]['q1'] += budget.q1
            customer_data[budget.customer]['q2'] += budget.q2
            customer_data[budget.customer]['q3'] += budget.q3
            customer_data[budget.customer]['q4'] += budget.q4

    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    budget_total = 0

    for customer in customer_data:
        jan_total += customer_data[customer]['jan']
        feb_total += customer_data[customer]['feb']
        mar_total += customer_data[customer]['mar']
        apr_total += customer_data[customer]['apr']
        may_total += customer_data[customer]['may']
        jun_total += customer_data[customer]['jun']
        jul_total += customer_data[customer]['jul']
        aug_total += customer_data[customer]['aug']
        sep_total += customer_data[customer]['sep']
        oct_total += customer_data[customer]['oct']
        nov_total += customer_data[customer]['nov']
        dec_total += customer_data[customer]['dec']
        q1_total += customer_data[customer]['q1']
        q2_total += customer_data[customer]['q2']
        q3_total += customer_data[customer]['q3']
        q4_total += customer_data[customer]['q4']
        budget_total += (customer_data[customer]['q1'] + customer_data[customer]['q2'] + customer_data[customer]['q3'] + customer_data[customer]['q4'])

    context = {
    'budget_data': customer_data,
    'first_col': 'customer',
    'region': budget_objects[0].location.region,
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'budget_total': budget_total,
    }
    return render(request, 'Ledger/budget.html', context)

################################################
########## BUDGET BY REGION BY SECTOR ##########
################################################

def cl_budget_region_sector(request): # Choose location

    regions = []
    for budget in Budget.objects.all().order_by('location__name'):
        if budget.location.region not in regions:
            regions.append(budget.location.region)
    
    context = {
        'locations': regions,
        'redirect': 'cy_budget_region_sector',
    }
    return render(request, 'Ledger/choose_location.html', context)

def cy_budget_region_sector(request, region_name_slug): # Choose year

    years = []

    for budget in Budget.objects.filter(location__region__slug=region_name_slug).order_by('year'):
        if budget.year not in years:
            years.append(budget.year)
    
    context = {
        'years': years,
        'location_name_slug': region_name_slug,
        'redirect': 'budget_region_sector',
    }
    return render(request, 'Ledger/choose_year.html', context)

def budget_region_sector(request, region_name_slug, year): # Budget table view

    # list of budgets corresponding to this plant and year
    budget_objects = Budget.objects.filter(location__region__slug=region_name_slug, year=year).order_by('customer__sector')
    
    sector_data = {} # create dictionary of data for each sector
    for budget in budget_objects:
        if budget.customer.sector not in sector_data.keys():
            sector_data[budget.customer.sector] = {
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
            sector_data[budget.customer.sector]['jan'] += budget.jan
            sector_data[budget.customer.sector]['feb'] += budget.feb
            sector_data[budget.customer.sector]['mar'] += budget.mar
            sector_data[budget.customer.sector]['apr'] += budget.apr
            sector_data[budget.customer.sector]['may'] += budget.may
            sector_data[budget.customer.sector]['jun'] += budget.jun
            sector_data[budget.customer.sector]['jul'] += budget.jul
            sector_data[budget.customer.sector]['aug'] += budget.aug
            sector_data[budget.customer.sector]['sep'] += budget.sep
            sector_data[budget.customer.sector]['oct'] += budget.oct
            sector_data[budget.customer.sector]['nov'] += budget.nov
            sector_data[budget.customer.sector]['dec'] += budget.dec
            sector_data[budget.customer.sector]['q1'] += budget.q1
            sector_data[budget.customer.sector]['q2'] += budget.q2
            sector_data[budget.customer.sector]['q3'] += budget.q3
            sector_data[budget.customer.sector]['q4'] += budget.q4
    
    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    budget_total = 0

    for sector in sector_data:
        jan_total += sector_data[sector]['jan']
        feb_total += sector_data[sector]['feb']
        mar_total += sector_data[sector]['mar']
        apr_total += sector_data[sector]['apr']
        may_total += sector_data[sector]['may']
        jun_total += sector_data[sector]['jun']
        jul_total += sector_data[sector]['jul']
        aug_total += sector_data[sector]['aug']
        sep_total += sector_data[sector]['sep']
        oct_total += sector_data[sector]['oct']
        nov_total += sector_data[sector]['nov']
        dec_total += sector_data[sector]['dec']
        q1_total += sector_data[sector]['q1']
        q2_total += sector_data[sector]['q2']
        q3_total += sector_data[sector]['q3']
        q4_total += sector_data[sector]['q4']
        budget_total += (sector_data[sector]['q1'] + sector_data[sector]['q2'] + sector_data[sector]['q3'] + sector_data[sector]['q4'])
    
    context = {
    'budget_data': sector_data,
    'first_col': 'sector',
    'region': budget_objects[0].location.region,
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'budget_total': budget_total,
    }
    return render(request, 'Ledger/budget.html', context)

###########################################
########## GLOBAL BUDGET BY PLANT ##########
###########################################

def cy_budget_global_plant(request): # Choose year
    
    years = []
    for budget in Budget.objects.all().order_by('year'):
        if budget.year not in years:
            years.append(budget.year)

    context = {
        'years': years,
        'redirect': 'budget_global_plant',
    }
    return render(request, 'Ledger/choose_year.html', context)

def budget_global_plant(request, year): # Budget table view
    
    budget_objects = Budget.objects.filter(year=year).order_by('location__name')

    plant_data = {} # create dictionary of data for each plant
    for budget in budget_objects:
        if budget.location not in plant_data.keys():
            plant_data[budget.location] = {
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
            plant_data[budget.location]['jan'] += budget.jan
            plant_data[budget.location]['feb'] += budget.feb
            plant_data[budget.location]['mar'] += budget.mar
            plant_data[budget.location]['apr'] += budget.apr
            plant_data[budget.location]['may'] += budget.may
            plant_data[budget.location]['jun'] += budget.jun
            plant_data[budget.location]['jul'] += budget.jul
            plant_data[budget.location]['aug'] += budget.aug
            plant_data[budget.location]['sep'] += budget.sep
            plant_data[budget.location]['oct'] += budget.oct
            plant_data[budget.location]['nov'] += budget.nov
            plant_data[budget.location]['dec'] += budget.dec
            plant_data[budget.location]['q1'] += budget.q1
            plant_data[budget.location]['q2'] += budget.q2
            plant_data[budget.location]['q3'] += budget.q3
            plant_data[budget.location]['q4'] += budget.q4

    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    budget_total = 0

    for plant in plant_data:
        jan_total += plant_data[plant]['jan']
        feb_total += plant_data[plant]['feb']
        mar_total += plant_data[plant]['mar']
        apr_total += plant_data[plant]['apr']
        may_total += plant_data[plant]['may']
        jun_total += plant_data[plant]['jun']
        jul_total += plant_data[plant]['jul']
        aug_total += plant_data[plant]['aug']
        sep_total += plant_data[plant]['sep']
        oct_total += plant_data[plant]['oct']
        nov_total += plant_data[plant]['nov']
        dec_total += plant_data[plant]['dec']
        q1_total += plant_data[plant]['q1']
        q2_total += plant_data[plant]['q2']
        q3_total += plant_data[plant]['q3']
        q4_total += plant_data[plant]['q4']
        budget_total += (plant_data[plant]['q1'] + plant_data[plant]['q2'] + plant_data[plant]['q3'] + plant_data[plant]['q4'])

    context = {
        'budget_data': plant_data,
        'global': True,
        'first_col': 'plant',
        'year': year,
        'jan_total': jan_total,
        'feb_total': feb_total,
        'mar_total': mar_total,
        'apr_total': apr_total,
        'may_total': may_total,
        'jun_total': jun_total,
        'jul_total': jul_total,
        'aug_total': aug_total,
        'sep_total': sep_total,
        'oct_total': oct_total,
        'nov_total': nov_total,
        'dec_total': dec_total,
        'q1_total': q1_total,
        'q2_total': q2_total,
        'q3_total': q3_total,
        'q4_total': q4_total,
        'budget_total': budget_total,
    }
    return render(request, 'Ledger/budget.html', context)

##############################################
########## GLOBAL BUDGET BY CUSTOMER ##########
##############################################

def cy_budget_global_customer(request): # Choose year

    years = []
    for budget in Budget.objects.all().order_by('year'):
        if budget.year not in years:
            years.append(budget.year)

    context = {
        'years': years,
        'redirect': 'budget_global_customer',
    }
    return render(request, 'Ledger/choose_year.html', context)

def budget_global_customer(request, year): # Budget table view

    budget_objects = Budget.objects.filter(year=year).order_by('customer__name')

    customer_data = {} # create dictionary of data for each customer
    for budget in budget_objects:
        if budget.customer not in customer_data.keys():
            customer_data[budget.customer] = {
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
            customer_data[budget.customer]['jan'] += budget.jan
            customer_data[budget.customer]['feb'] += budget.feb
            customer_data[budget.customer]['mar'] += budget.mar
            customer_data[budget.customer]['apr'] += budget.apr
            customer_data[budget.customer]['may'] += budget.may
            customer_data[budget.customer]['jun'] += budget.jun
            customer_data[budget.customer]['jul'] += budget.jul
            customer_data[budget.customer]['aug'] += budget.aug
            customer_data[budget.customer]['sep'] += budget.sep
            customer_data[budget.customer]['oct'] += budget.oct
            customer_data[budget.customer]['nov'] += budget.nov
            customer_data[budget.customer]['dec'] += budget.dec
            customer_data[budget.customer]['q1'] += budget.q1
            customer_data[budget.customer]['q2'] += budget.q2
            customer_data[budget.customer]['q3'] += budget.q3
            customer_data[budget.customer]['q4'] += budget.q4

    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    budget_total = 0

    for customer in customer_data:
        jan_total += customer_data[customer]['jan']
        feb_total += customer_data[customer]['feb']
        mar_total += customer_data[customer]['mar']
        apr_total += customer_data[customer]['apr']
        may_total += customer_data[customer]['may']
        jun_total += customer_data[customer]['jun']
        jul_total += customer_data[customer]['jul']
        aug_total += customer_data[customer]['aug']
        sep_total += customer_data[customer]['sep']
        oct_total += customer_data[customer]['oct']
        nov_total += customer_data[customer]['nov']
        dec_total += customer_data[customer]['dec']
        q1_total += customer_data[customer]['q1']
        q2_total += customer_data[customer]['q2']
        q3_total += customer_data[customer]['q3']
        q4_total += customer_data[customer]['q4']
        budget_total += (customer_data[customer]['q1'] + customer_data[customer]['q2'] + customer_data[customer]['q3'] + customer_data[customer]['q4'])

    context = {
    'budget_data': customer_data,
    'first_col': 'customer',
    'global': True,
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'budget_total': budget_total,
    }
    return render(request, 'Ledger/budget.html', context)

############################################
########## GLOBAL BUDGET BY SECTOR ##########
############################################

def cy_budget_global_sector(request): # Choose year

    years = []
    for budget in Budget.objects.all().order_by('year'):
        if budget.year not in years:
            years.append(budget.year)

    context = {
        'years': years,
        'redirect': 'budget_global_sector',
    }
    return render(request, 'Ledger/choose_year.html', context)

def budget_global_sector(request, year): # Budget table view
    
    budget_objects = Budget.objects.filter(year=year).order_by('customer__sector')

    sector_data = {} # create dictionary of data for each sector
    for budget in budget_objects:
        if budget.customer.sector not in sector_data.keys():
            sector_data[budget.customer.sector] = {
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
            sector_data[budget.customer.sector]['jan'] += budget.jan
            sector_data[budget.customer.sector]['feb'] += budget.feb
            sector_data[budget.customer.sector]['mar'] += budget.mar
            sector_data[budget.customer.sector]['apr'] += budget.apr
            sector_data[budget.customer.sector]['may'] += budget.may
            sector_data[budget.customer.sector]['jun'] += budget.jun
            sector_data[budget.customer.sector]['jul'] += budget.jul
            sector_data[budget.customer.sector]['aug'] += budget.aug
            sector_data[budget.customer.sector]['sep'] += budget.sep
            sector_data[budget.customer.sector]['oct'] += budget.oct
            sector_data[budget.customer.sector]['nov'] += budget.nov
            sector_data[budget.customer.sector]['dec'] += budget.dec
            sector_data[budget.customer.sector]['q1'] += budget.q1
            sector_data[budget.customer.sector]['q2'] += budget.q2
            sector_data[budget.customer.sector]['q3'] += budget.q3
            sector_data[budget.customer.sector]['q4'] += budget.q4
    
    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    budget_total = 0

    for sector in sector_data:
        jan_total += sector_data[sector]['jan']
        feb_total += sector_data[sector]['feb']
        mar_total += sector_data[sector]['mar']
        apr_total += sector_data[sector]['apr']
        may_total += sector_data[sector]['may']
        jun_total += sector_data[sector]['jun']
        jul_total += sector_data[sector]['jul']
        aug_total += sector_data[sector]['aug']
        sep_total += sector_data[sector]['sep']
        oct_total += sector_data[sector]['oct']
        nov_total += sector_data[sector]['nov']
        dec_total += sector_data[sector]['dec']
        q1_total += sector_data[sector]['q1']
        q2_total += sector_data[sector]['q2']
        q3_total += sector_data[sector]['q3']
        q4_total += sector_data[sector]['q4']
        budget_total += (sector_data[sector]['q1'] + sector_data[sector]['q2'] + sector_data[sector]['q3'] + sector_data[sector]['q4'])
    
    context = {
    'budget_data': sector_data,
    'first_col': 'sector',
    'global': True,
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'budget_total': budget_total,
    }
    return render(request, 'Ledger/budget.html', context)

############################################
########## GLOBAL BUDGET BY REGION ##########
############################################

def cy_budget_global_region(request): # Choose year

    years = []
    for budget in Budget.objects.all().order_by('year'):
        if budget.year not in years:
            years.append(budget.year)

    context = {
        'years': years,
        'redirect': 'budget_global_region',
    }
    return render(request, 'Ledger/choose_year.html', context)

def budget_global_region(request, year): # Budget table view
    
    budget_objects = Budget.objects.filter(year=year).order_by('location__region')

    region_data = {} # create dictionary of data for each region
    for budget in budget_objects:
        if budget.location.region not in region_data.keys():
            region_data[budget.location.region] = {
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
            region_data[budget.location.region]['jan'] += budget.jan
            region_data[budget.location.region]['feb'] += budget.feb
            region_data[budget.location.region]['mar'] += budget.mar
            region_data[budget.location.region]['apr'] += budget.apr
            region_data[budget.location.region]['may'] += budget.may
            region_data[budget.location.region]['jun'] += budget.jun
            region_data[budget.location.region]['jul'] += budget.jul
            region_data[budget.location.region]['aug'] += budget.aug
            region_data[budget.location.region]['sep'] += budget.sep
            region_data[budget.location.region]['oct'] += budget.oct
            region_data[budget.location.region]['nov'] += budget.nov
            region_data[budget.location.region]['dec'] += budget.dec
            region_data[budget.location.region]['q1'] += budget.q1
            region_data[budget.location.region]['q2'] += budget.q2
            region_data[budget.location.region]['q3'] += budget.q3
            region_data[budget.location.region]['q4'] += budget.q4

    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    budget_total = 0

    for region in region_data:
        jan_total += region_data[region]['jan']
        feb_total += region_data[region]['feb']
        mar_total += region_data[region]['mar']
        apr_total += region_data[region]['apr']
        may_total += region_data[region]['may']
        jun_total += region_data[region]['jun']
        jul_total += region_data[region]['jul']
        aug_total += region_data[region]['aug']
        sep_total += region_data[region]['sep']
        oct_total += region_data[region]['oct']
        nov_total += region_data[region]['nov']
        dec_total += region_data[region]['dec']
        q1_total += region_data[region]['q1']
        q2_total += region_data[region]['q2']
        q3_total += region_data[region]['q3']
        q4_total += region_data[region]['q4']
        budget_total += (region_data[region]['q1'] + region_data[region]['q2'] + region_data[region]['q3'] + region_data[region]['q4'])
    context = {
    'budget_data': region_data,
    'first_col': 'region',
    'global': True,
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'budget_total': budget_total,
    }
    return render(request, 'Ledger/budget.html', context)

#################################################
########## ACTUALS BY CUSTOMER BY PLANT ##########
#################################################

def cc_sale_customer_plant(request): #Choose customer
    customers = []
    for sale in Sale.objects.all().order_by('customer__name'):
        if sale.customer not in customers:
            customers.append(sale.customer)

    context = {
        'customers': customers,
        'redirect': 'cy_sale_customer_plant',
    }
    return render(request, 'Ledger/choose_customer.html', context)

def cy_sale_customer_plant(request, customer_name_slug):

    years = []

    for sale in Sale.objects.filter(customer__slug=customer_name_slug).order_by('year'):
        if sale.year not in years:
            years.append(sale.year)

    context = {
        'years': years,
        'location_name_slug': customer_name_slug,
        'redirect': 'sale_customer_plant',
    }
    return render(request, 'Ledger/choose_year.html', context)

def sale_customer_plant(request, customer_name_slug, year):
    
    sale_objects = Sale.objects.filter(customer__slug=customer_name_slug, year=year)

    plant_data = {}
    for sale in sale_objects:
        if sale.location not in plant_data.keys():
            plant_data[sale.location] = {
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
            plant_data[sale.location]['jan'] += sale.jan
            plant_data[sale.location]['feb'] += sale.feb
            plant_data[sale.location]['mar'] += sale.mar
            plant_data[sale.location]['apr'] += sale.apr
            plant_data[sale.location]['may'] += sale.may
            plant_data[sale.location]['jun'] += sale.jun
            plant_data[sale.location]['jul'] += sale.jul
            plant_data[sale.location]['aug'] += sale.aug
            plant_data[sale.location]['sep'] += sale.sep
            plant_data[sale.location]['oct'] += sale.oct
            plant_data[sale.location]['nov'] += sale.nov
            plant_data[sale.location]['dec'] += sale.dec
            plant_data[sale.location]['q1'] += sale.q1
            plant_data[sale.location]['q2'] += sale.q2
            plant_data[sale.location]['q3'] += sale.q3
            plant_data[sale.location]['q4'] += sale.q4

    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    sale_total = 0

    for plant in plant_data:
        jan_total += plant_data[plant]['jan']
        feb_total += plant_data[plant]['feb']
        mar_total += plant_data[plant]['mar']
        apr_total += plant_data[plant]['apr']
        may_total += plant_data[plant]['may']
        jun_total += plant_data[plant]['jun']
        jul_total += plant_data[plant]['jul']
        aug_total += plant_data[plant]['aug']
        sep_total += plant_data[plant]['sep']
        oct_total += plant_data[plant]['oct']
        nov_total += plant_data[plant]['nov']
        dec_total += plant_data[plant]['dec']
        q1_total += plant_data[plant]['q1']
        q2_total += plant_data[plant]['q2']
        q3_total += plant_data[plant]['q3']
        q4_total += plant_data[plant]['q4']
        sale_total += (plant_data[plant]['q1'] + plant_data[plant]['q2'] + plant_data[plant]['q3'] + plant_data[plant]['q4'])

    context = {
    'sale_data': plant_data,
    'first_col': 'plant',
    'customer': Customer.objects.get(slug=customer_name_slug),
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'sale_total': sale_total,
    }
    return render(request, 'Ledger/sale.html', context)

##################################################
########## ACTUALS BY PLANT BY CUSTOMER ##########
##################################################

def cl_sale_plant_customer(request):

    sale_locations = []
    for sale in Sale.objects.all().order_by('location__name'):
        if sale.location not in sale_locations:
            sale_locations.append(sale.location)

    context = {
        'locations': sale_locations,
        'redirect': 'cy_sale_plant_customer',
    }
    return render(request, 'Ledger/choose_location.html', context)

def cy_sale_plant_customer(request, location_name_slug):

    years = []

    for sale in Sale.objects.filter(location__slug=location_name_slug).order_by('year'):
        if sale.year not in years:
            years.append(sale.year)

    context = {
        'years': years,
        'location_name_slug': location_name_slug,
        'redirect': 'sale_plant_customer',
    }
    return render(request, 'Ledger/choose_year.html', context)

def sale_plant_customer(request, location_name_slug, year):

    sale_objects = Sale.objects.filter(location__slug=location_name_slug, year=year).order_by('customer__name')

    location = sale_objects[0].location
    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    sale_total = 0

    for sale in sale_objects:
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
    
    context = {
        'sale_objects': sale_objects,
        'first_col': 'customer',
        'second_col': 'sector',
        'location': location,
        'year': year,
        'jan_total': jan_total,
        'feb_total': feb_total,
        'mar_total': mar_total,
        'apr_total': apr_total,
        'may_total': may_total,
        'jun_total': jun_total,
        'jul_total': jul_total,
        'aug_total': aug_total,
        'sep_total': sep_total,
        'oct_total': oct_total,
        'nov_total': nov_total,
        'dec_total': dec_total,
        'q1_total': q1_total,
        'q2_total': q2_total,
        'q3_total': q3_total,
        'q4_total': q4_total,
        'sale_total': sale_total,
    }
    return render(request, 'Ledger/sale.html', context)

################################################
########## ACTUALS BY PLANT BY SECTOR ##########
################################################

def cl_sale_plant_sector(request):

    sale_locations = []
    for sale in Sale.objects.all().order_by('location__name'):
        if sale.location not in sale_locations:
            sale_locations.append(sale.location)

    context = {
        'locations': sale_locations,
        'redirect': 'cy_sale_plant_sector',
    }
    return render(request, 'Ledger/choose_location.html', context)

def cy_sale_plant_sector(request, location_name_slug):

    years = []

    for sale in Sale.objects.filter(location__slug=location_name_slug).order_by('year'):
        if sale.year not in years:
            years.append(sale.year)

    context = {
        'years': years,
        'location_name_slug': location_name_slug,
        'redirect': 'sale_plant_sector',
    }
    return render(request, 'Ledger/choose_year.html', context)

def sale_plant_sector(request, location_name_slug, year):

    sale_objects = Sale.objects.filter(location__slug=location_name_slug, year=year).order_by('customer__sector')
    
    sector_data = {} # create dictionary of data for each sector
    for sale in sale_objects:
        if sale.customer.sector not in sector_data.keys():
            sector_data[sale.customer.sector] = {
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
            sector_data[sale.customer.sector]['jan'] += sale.jan
            sector_data[sale.customer.sector]['feb'] += sale.feb
            sector_data[sale.customer.sector]['mar'] += sale.mar
            sector_data[sale.customer.sector]['apr'] += sale.apr
            sector_data[sale.customer.sector]['may'] += sale.may
            sector_data[sale.customer.sector]['jun'] += sale.jun
            sector_data[sale.customer.sector]['jul'] += sale.jul
            sector_data[sale.customer.sector]['aug'] += sale.aug
            sector_data[sale.customer.sector]['sep'] += sale.sep
            sector_data[sale.customer.sector]['oct'] += sale.oct
            sector_data[sale.customer.sector]['nov'] += sale.nov
            sector_data[sale.customer.sector]['dec'] += sale.dec
            sector_data[sale.customer.sector]['q1'] += sale.q1
            sector_data[sale.customer.sector]['q2'] += sale.q2
            sector_data[sale.customer.sector]['q3'] += sale.q3
            sector_data[sale.customer.sector]['q4'] += sale.q4

    location = sale_objects[0].location
    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    sale_total = 0

    for sector in sector_data:
        jan_total += sector_data[sector]['jan']
        feb_total += sector_data[sector]['feb']
        mar_total += sector_data[sector]['mar']
        apr_total += sector_data[sector]['apr']
        may_total += sector_data[sector]['may']
        jun_total += sector_data[sector]['jun']
        jul_total += sector_data[sector]['jul']
        aug_total += sector_data[sector]['aug']
        sep_total += sector_data[sector]['sep']
        oct_total += sector_data[sector]['oct']
        nov_total += sector_data[sector]['nov']
        dec_total += sector_data[sector]['dec']
        q1_total += sector_data[sector]['q1']
        q2_total += sector_data[sector]['q2']
        q3_total += sector_data[sector]['q3']
        q4_total += sector_data[sector]['q4']
        sale_total += (sector_data[sector]['q1'] + sector_data[sector]['q2'] + sector_data[sector]['q3'] + sector_data[sector]['q4'])
    
    context = {
    'sale_data': sector_data,
    'first_col': 'sector',
    'location': location,
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'sale_total': sale_total,
    }
    return render(request, 'Ledger/sale.html', context)

################################################
########## ACTUALS BY REGION BY PLANT ##########
################################################

def cl_sale_region_plant(request):

    regions = []
    for sale in Sale.objects.all().order_by('location__name'):
        if sale.location.region not in regions:
            regions.append(sale.location.region)
    
    context = {
        'locations': regions,
        'redirect': 'cy_sale_region_plant',
    }
    return render(request, 'Ledger/choose_location.html', context)

def cy_sale_region_plant(request, region_name_slug):

    years = []

    for sale in Sale.objects.filter(location__region__slug=region_name_slug).order_by('year'):
        if sale.year not in years:
            years.append(sale.year)
    
    context = {
        'years': years,
        'location_name_slug': region_name_slug,
        'redirect': 'sale_region_plant',
    }
    return render(request, 'Ledger/choose_year.html', context)

def sale_region_plant(request, region_name_slug, year):
    
    sale_objects = Sale.objects.filter(location__region__slug=region_name_slug, year=year).order_by('location__name')

    plant_data = {} # create dictionary of data for each plant
    for sale in sale_objects:
        if sale.location not in plant_data.keys():
            plant_data[sale.location] = {
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
            plant_data[sale.location]['jan'] += sale.jan
            plant_data[sale.location]['feb'] += sale.feb
            plant_data[sale.location]['mar'] += sale.mar
            plant_data[sale.location]['apr'] += sale.apr
            plant_data[sale.location]['may'] += sale.may
            plant_data[sale.location]['jun'] += sale.jun
            plant_data[sale.location]['jul'] += sale.jul
            plant_data[sale.location]['aug'] += sale.aug
            plant_data[sale.location]['sep'] += sale.sep
            plant_data[sale.location]['oct'] += sale.oct
            plant_data[sale.location]['nov'] += sale.nov
            plant_data[sale.location]['dec'] += sale.dec
            plant_data[sale.location]['q1'] += sale.q1
            plant_data[sale.location]['q2'] += sale.q2
            plant_data[sale.location]['q3'] += sale.q3
            plant_data[sale.location]['q4'] += sale.q4

    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    sale_total = 0

    for plant in plant_data:
        jan_total += plant_data[plant]['jan']
        feb_total += plant_data[plant]['feb']
        mar_total += plant_data[plant]['mar']
        apr_total += plant_data[plant]['apr']
        may_total += plant_data[plant]['may']
        jun_total += plant_data[plant]['jun']
        jul_total += plant_data[plant]['jul']
        aug_total += plant_data[plant]['aug']
        sep_total += plant_data[plant]['sep']
        oct_total += plant_data[plant]['oct']
        nov_total += plant_data[plant]['nov']
        dec_total += plant_data[plant]['dec']
        q1_total += plant_data[plant]['q1']
        q2_total += plant_data[plant]['q2']
        q3_total += plant_data[plant]['q3']
        q4_total += plant_data[plant]['q4']
        sale_total += (plant_data[plant]['q1'] + plant_data[plant]['q2'] + plant_data[plant]['q3'] + plant_data[plant]['q4'])

    context = {
        'sale_data': plant_data,
        'first_col': 'plant',
        'region': sale_objects[0].location.region,
        'year': year,
        'jan_total': jan_total,
        'feb_total': feb_total,
        'mar_total': mar_total,
        'apr_total': apr_total,
        'may_total': may_total,
        'jun_total': jun_total,
        'jul_total': jul_total,
        'aug_total': aug_total,
        'sep_total': sep_total,
        'oct_total': oct_total,
        'nov_total': nov_total,
        'dec_total': dec_total,
        'q1_total': q1_total,
        'q2_total': q2_total,
        'q3_total': q3_total,
        'q4_total': q4_total,
        'sale_total': sale_total,
    }
    return render(request, 'Ledger/sale.html', context)

###################################################
########## ACTUALS BY REGION BY CUSTOMER ##########
###################################################

def cl_sale_region_customer(request):

    regions = []
    for sale in Sale.objects.all().order_by('location__name'):
        if sale.location.region not in regions:
            regions.append(sale.location.region)
    
    context = {
        'locations': regions,
        'redirect': 'cy_sale_region_customer',
    }
    return render(request, 'Ledger/choose_location.html', context)

def cy_sale_region_customer(request, region_name_slug):

    years = []

    for sale in Sale.objects.filter(location__region__slug=region_name_slug).order_by('year'):
        if sale.year not in years:
            years.append(sale.year)
    
    context = {
        'years': years,
        'location_name_slug': region_name_slug,
        'redirect': 'sale_region_customer',
    }
    return render(request, 'Ledger/choose_year.html', context)

def sale_region_customer(request, region_name_slug, year):

    sale_objects = Sale.objects.filter(location__region__slug=region_name_slug, year=year).order_by('customer__name')

    customer_data = {} # create dictionary of data for each customer
    for sale in sale_objects:
        if sale.customer not in customer_data.keys():
            customer_data[sale.customer] = {
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
            customer_data[sale.customer]['jan'] += sale.jan
            customer_data[sale.customer]['feb'] += sale.feb
            customer_data[sale.customer]['mar'] += sale.mar
            customer_data[sale.customer]['apr'] += sale.apr
            customer_data[sale.customer]['may'] += sale.may
            customer_data[sale.customer]['jun'] += sale.jun
            customer_data[sale.customer]['jul'] += sale.jul
            customer_data[sale.customer]['aug'] += sale.aug
            customer_data[sale.customer]['sep'] += sale.sep
            customer_data[sale.customer]['oct'] += sale.oct
            customer_data[sale.customer]['nov'] += sale.nov
            customer_data[sale.customer]['dec'] += sale.dec
            customer_data[sale.customer]['q1'] += sale.q1
            customer_data[sale.customer]['q2'] += sale.q2
            customer_data[sale.customer]['q3'] += sale.q3
            customer_data[sale.customer]['q4'] += sale.q4

    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    sale_total = 0

    for customer in customer_data:
        jan_total += customer_data[customer]['jan']
        feb_total += customer_data[customer]['feb']
        mar_total += customer_data[customer]['mar']
        apr_total += customer_data[customer]['apr']
        may_total += customer_data[customer]['may']
        jun_total += customer_data[customer]['jun']
        jul_total += customer_data[customer]['jul']
        aug_total += customer_data[customer]['aug']
        sep_total += customer_data[customer]['sep']
        oct_total += customer_data[customer]['oct']
        nov_total += customer_data[customer]['nov']
        dec_total += customer_data[customer]['dec']
        q1_total += customer_data[customer]['q1']
        q2_total += customer_data[customer]['q2']
        q3_total += customer_data[customer]['q3']
        q4_total += customer_data[customer]['q4']
        sale_total += (customer_data[customer]['q1'] + customer_data[customer]['q2'] + customer_data[customer]['q3'] + customer_data[customer]['q4'])

    context = {
    'sale_data': customer_data,
    'first_col': 'customer',
    'region': sale_objects[0].location.region,
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'sale_total': sale_total,
    }
    return render(request, 'Ledger/sale.html', context)

#################################################
########## ACTUALS BY REGION BY SECTOR ##########
#################################################

def cl_sale_region_sector(request):

    regions = []
    for sale in Sale.objects.all().order_by('location__name'):
        if sale.location.region not in regions:
            regions.append(sale.location.region)
    
    context = {
        'locations': regions,
        'redirect': 'cy_sale_region_sector',
    }
    return render(request, 'Ledger/choose_location.html', context)

def cy_sale_region_sector(request, region_name_slug):

    years = []

    for sale in Sale.objects.filter(location__region__slug=region_name_slug).order_by('year'):
        if sale.year not in years:
            years.append(sale.year)
    
    context = {
        'years': years,
        'location_name_slug': region_name_slug,
        'redirect': 'sale_region_sector',
    }
    return render(request, 'Ledger/choose_year.html', context)

def sale_region_sector(request, region_name_slug, year):
    
    sale_objects = Sale.objects.filter(location__region__slug=region_name_slug, year=year).order_by('customer__sector')
    
    sector_data = {} # create dictionary of data for each sector
    for sale in sale_objects:
        if sale.customer.sector not in sector_data.keys():
            sector_data[sale.customer.sector] = {
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
            sector_data[sale.customer.sector]['jan'] += sale.jan
            sector_data[sale.customer.sector]['feb'] += sale.feb
            sector_data[sale.customer.sector]['mar'] += sale.mar
            sector_data[sale.customer.sector]['apr'] += sale.apr
            sector_data[sale.customer.sector]['may'] += sale.may
            sector_data[sale.customer.sector]['jun'] += sale.jun
            sector_data[sale.customer.sector]['jul'] += sale.jul
            sector_data[sale.customer.sector]['aug'] += sale.aug
            sector_data[sale.customer.sector]['sep'] += sale.sep
            sector_data[sale.customer.sector]['oct'] += sale.oct
            sector_data[sale.customer.sector]['nov'] += sale.nov
            sector_data[sale.customer.sector]['dec'] += sale.dec
            sector_data[sale.customer.sector]['q1'] += sale.q1
            sector_data[sale.customer.sector]['q2'] += sale.q2
            sector_data[sale.customer.sector]['q3'] += sale.q3
            sector_data[sale.customer.sector]['q4'] += sale.q4
    
    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    sale_total = 0

    for sector in sector_data:
        jan_total += sector_data[sector]['jan']
        feb_total += sector_data[sector]['feb']
        mar_total += sector_data[sector]['mar']
        apr_total += sector_data[sector]['apr']
        may_total += sector_data[sector]['may']
        jun_total += sector_data[sector]['jun']
        jul_total += sector_data[sector]['jul']
        aug_total += sector_data[sector]['aug']
        sep_total += sector_data[sector]['sep']
        oct_total += sector_data[sector]['oct']
        nov_total += sector_data[sector]['nov']
        dec_total += sector_data[sector]['dec']
        q1_total += sector_data[sector]['q1']
        q2_total += sector_data[sector]['q2']
        q3_total += sector_data[sector]['q3']
        q4_total += sector_data[sector]['q4']
        sale_total += (sector_data[sector]['q1'] + sector_data[sector]['q2'] + sector_data[sector]['q3'] + sector_data[sector]['q4'])
    
    context = {
    'sale_data': sector_data,
    'first_col': 'sector',
    'region': sale_objects[0].location.region,
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'sale_total': sale_total,
    }
    return render(request, 'Ledger/sale.html', context)

###########################################
########## GLOBAL SALES BY PLANT ##########
###########################################

def cy_sale_global_plant(request):

    years = []
    for sale in Sale.objects.all().order_by('year'):
        if sale.year not in years:
            years.append(sale.year)

    context = {
        'years': years,
        'redirect': 'sale_global_plant',
    }
    return render(request, 'Ledger/choose_year.html', context)

def sale_global_plant(request, year):

    sale_objects = Sale.objects.filter(year=year).order_by('location__name')

    plant_data = {} # create dictionary of data for each plant
    for sale in sale_objects:
        if sale.location not in plant_data.keys():
            plant_data[sale.location] = {
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
            plant_data[sale.location]['jan'] += sale.jan
            plant_data[sale.location]['feb'] += sale.feb
            plant_data[sale.location]['mar'] += sale.mar
            plant_data[sale.location]['apr'] += sale.apr
            plant_data[sale.location]['may'] += sale.may
            plant_data[sale.location]['jun'] += sale.jun
            plant_data[sale.location]['jul'] += sale.jul
            plant_data[sale.location]['aug'] += sale.aug
            plant_data[sale.location]['sep'] += sale.sep
            plant_data[sale.location]['oct'] += sale.oct
            plant_data[sale.location]['nov'] += sale.nov
            plant_data[sale.location]['dec'] += sale.dec
            plant_data[sale.location]['q1'] += sale.q1
            plant_data[sale.location]['q2'] += sale.q2
            plant_data[sale.location]['q3'] += sale.q3
            plant_data[sale.location]['q4'] += sale.q4

    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    sale_total = 0

    for plant in plant_data:
        jan_total += plant_data[plant]['jan']
        feb_total += plant_data[plant]['feb']
        mar_total += plant_data[plant]['mar']
        apr_total += plant_data[plant]['apr']
        may_total += plant_data[plant]['may']
        jun_total += plant_data[plant]['jun']
        jul_total += plant_data[plant]['jul']
        aug_total += plant_data[plant]['aug']
        sep_total += plant_data[plant]['sep']
        oct_total += plant_data[plant]['oct']
        nov_total += plant_data[plant]['nov']
        dec_total += plant_data[plant]['dec']
        q1_total += plant_data[plant]['q1']
        q2_total += plant_data[plant]['q2']
        q3_total += plant_data[plant]['q3']
        q4_total += plant_data[plant]['q4']
        sale_total += (plant_data[plant]['q1'] + plant_data[plant]['q2'] + plant_data[plant]['q3'] + plant_data[plant]['q4'])

    context = {
        'sale_data': plant_data,
        'global': True,
        'first_col': 'plant',
        'year': year,
        'jan_total': jan_total,
        'feb_total': feb_total,
        'mar_total': mar_total,
        'apr_total': apr_total,
        'may_total': may_total,
        'jun_total': jun_total,
        'jul_total': jul_total,
        'aug_total': aug_total,
        'sep_total': sep_total,
        'oct_total': oct_total,
        'nov_total': nov_total,
        'dec_total': dec_total,
        'q1_total': q1_total,
        'q2_total': q2_total,
        'q3_total': q3_total,
        'q4_total': q4_total,
        'sale_total': sale_total,
    }
    return render(request, 'Ledger/sale.html', context)

##############################################
########## GLOBAL SALES BY CUSTOMER ##########
##############################################

def cy_sale_global_customer(request):

    years = []
    for sale in Sale.objects.all().order_by('year'):
        if sale.year not in years:
            years.append(sale.year)

    context = {
        'years': years,
        'redirect': 'sale_global_customer',
    }
    return render(request, 'Ledger/choose_year.html', context)

def sale_global_customer(request, year):

    sale_objects = Sale.objects.filter(year=year).order_by('customer__name')

    customer_data = {} # create dictionary of data for each customer
    for sale in sale_objects:
        if sale.customer not in customer_data.keys():
            customer_data[sale.customer] = {
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
            customer_data[sale.customer]['jan'] += sale.jan
            customer_data[sale.customer]['feb'] += sale.feb
            customer_data[sale.customer]['mar'] += sale.mar
            customer_data[sale.customer]['apr'] += sale.apr
            customer_data[sale.customer]['may'] += sale.may
            customer_data[sale.customer]['jun'] += sale.jun
            customer_data[sale.customer]['jul'] += sale.jul
            customer_data[sale.customer]['aug'] += sale.aug
            customer_data[sale.customer]['sep'] += sale.sep
            customer_data[sale.customer]['oct'] += sale.oct
            customer_data[sale.customer]['nov'] += sale.nov
            customer_data[sale.customer]['dec'] += sale.dec
            customer_data[sale.customer]['q1'] += sale.q1
            customer_data[sale.customer]['q2'] += sale.q2
            customer_data[sale.customer]['q3'] += sale.q3
            customer_data[sale.customer]['q4'] += sale.q4

    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    sale_total = 0

    for customer in customer_data:
        jan_total += customer_data[customer]['jan']
        feb_total += customer_data[customer]['feb']
        mar_total += customer_data[customer]['mar']
        apr_total += customer_data[customer]['apr']
        may_total += customer_data[customer]['may']
        jun_total += customer_data[customer]['jun']
        jul_total += customer_data[customer]['jul']
        aug_total += customer_data[customer]['aug']
        sep_total += customer_data[customer]['sep']
        oct_total += customer_data[customer]['oct']
        nov_total += customer_data[customer]['nov']
        dec_total += customer_data[customer]['dec']
        q1_total += customer_data[customer]['q1']
        q2_total += customer_data[customer]['q2']
        q3_total += customer_data[customer]['q3']
        q4_total += customer_data[customer]['q4']
        sale_total += (customer_data[customer]['q1'] + customer_data[customer]['q2'] + customer_data[customer]['q3'] + customer_data[customer]['q4'])

    context = {
    'sale_data': customer_data,
    'first_col': 'customer',
    'global': True,
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'sale_total': sale_total,
    }
    return render(request, 'Ledger/sale.html', context)

############################################
########## GLOBAL SALES BY SECTOR ##########
############################################

def cy_sale_global_sector(request):

    years = []
    for sale in Sale.objects.all().order_by('year'):
        if sale.year not in years:
            years.append(sale.year)

    context = {
        'years': years,
        'redirect': 'sale_global_sector',
    }
    return render(request, 'Ledger/choose_year.html', context)

def sale_global_sector(request, year):

    sale_objects = Sale.objects.filter(year=year).order_by('customer__sector')

    sector_data = {} # create dictionary of data for each sector
    for sale in sale_objects:
        if sale.customer.sector not in sector_data.keys():
            sector_data[sale.customer.sector] = {
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
            sector_data[sale.customer.sector]['jan'] += sale.jan
            sector_data[sale.customer.sector]['feb'] += sale.feb
            sector_data[sale.customer.sector]['mar'] += sale.mar
            sector_data[sale.customer.sector]['apr'] += sale.apr
            sector_data[sale.customer.sector]['may'] += sale.may
            sector_data[sale.customer.sector]['jun'] += sale.jun
            sector_data[sale.customer.sector]['jul'] += sale.jul
            sector_data[sale.customer.sector]['aug'] += sale.aug
            sector_data[sale.customer.sector]['sep'] += sale.sep
            sector_data[sale.customer.sector]['oct'] += sale.oct
            sector_data[sale.customer.sector]['nov'] += sale.nov
            sector_data[sale.customer.sector]['dec'] += sale.dec
            sector_data[sale.customer.sector]['q1'] += sale.q1
            sector_data[sale.customer.sector]['q2'] += sale.q2
            sector_data[sale.customer.sector]['q3'] += sale.q3
            sector_data[sale.customer.sector]['q4'] += sale.q4
    
    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    sale_total = 0

    for sector in sector_data:
        jan_total += sector_data[sector]['jan']
        feb_total += sector_data[sector]['feb']
        mar_total += sector_data[sector]['mar']
        apr_total += sector_data[sector]['apr']
        may_total += sector_data[sector]['may']
        jun_total += sector_data[sector]['jun']
        jul_total += sector_data[sector]['jul']
        aug_total += sector_data[sector]['aug']
        sep_total += sector_data[sector]['sep']
        oct_total += sector_data[sector]['oct']
        nov_total += sector_data[sector]['nov']
        dec_total += sector_data[sector]['dec']
        q1_total += sector_data[sector]['q1']
        q2_total += sector_data[sector]['q2']
        q3_total += sector_data[sector]['q3']
        q4_total += sector_data[sector]['q4']
        sale_total += (sector_data[sector]['q1'] + sector_data[sector]['q2'] + sector_data[sector]['q3'] + sector_data[sector]['q4'])
    
    context = {
    'sale_data': sector_data,
    'first_col': 'sector',
    'global': True,
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'sale_total': sale_total,
    }
    return render(request, 'Ledger/sale.html', context)

############################################
########## GLOBAL SALES BY REGION ##########
############################################

def cy_sale_global_region(request):

    years = []
    for sale in Sale.objects.all().order_by('year'):
        if sale.year not in years:
            years.append(sale.year)

    context = {
        'years': years,
        'redirect': 'sale_global_region',
    }
    return render(request, 'Ledger/choose_year.html', context)

def sale_global_region(request, year):

    sale_objects = Sale.objects.filter(year=year).order_by('location__region')

    region_data = {} # create dictionary of data for each region
    for sale in sale_objects:
        if sale.location.region not in region_data.keys():
            region_data[sale.location.region] = {
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
            region_data[sale.location.region]['jan'] += sale.jan
            region_data[sale.location.region]['feb'] += sale.feb
            region_data[sale.location.region]['mar'] += sale.mar
            region_data[sale.location.region]['apr'] += sale.apr
            region_data[sale.location.region]['may'] += sale.may
            region_data[sale.location.region]['jun'] += sale.jun
            region_data[sale.location.region]['jul'] += sale.jul
            region_data[sale.location.region]['aug'] += sale.aug
            region_data[sale.location.region]['sep'] += sale.sep
            region_data[sale.location.region]['oct'] += sale.oct
            region_data[sale.location.region]['nov'] += sale.nov
            region_data[sale.location.region]['dec'] += sale.dec
            region_data[sale.location.region]['q1'] += sale.q1
            region_data[sale.location.region]['q2'] += sale.q2
            region_data[sale.location.region]['q3'] += sale.q3
            region_data[sale.location.region]['q4'] += sale.q4

    jan_total = 0
    feb_total = 0
    mar_total = 0
    apr_total = 0
    may_total = 0
    jun_total = 0
    jul_total = 0
    aug_total = 0
    sep_total = 0
    oct_total = 0
    nov_total = 0
    dec_total = 0
    q1_total = 0
    q2_total = 0
    q3_total = 0
    q4_total = 0
    sale_total = 0

    for region in region_data:
        jan_total += region_data[region]['jan']
        feb_total += region_data[region]['feb']
        mar_total += region_data[region]['mar']
        apr_total += region_data[region]['apr']
        may_total += region_data[region]['may']
        jun_total += region_data[region]['jun']
        jul_total += region_data[region]['jul']
        aug_total += region_data[region]['aug']
        sep_total += region_data[region]['sep']
        oct_total += region_data[region]['oct']
        nov_total += region_data[region]['nov']
        dec_total += region_data[region]['dec']
        q1_total += region_data[region]['q1']
        q2_total += region_data[region]['q2']
        q3_total += region_data[region]['q3']
        q4_total += region_data[region]['q4']
        sale_total += (region_data[region]['q1'] + region_data[region]['q2'] + region_data[region]['q3'] + region_data[region]['q4'])
    context = {
    'sale_data': region_data,
    'first_col': 'region',
    'global': True,
    'year': year,
    'jan_total': jan_total,
    'feb_total': feb_total,
    'mar_total': mar_total,
    'apr_total': apr_total,
    'may_total': may_total,
    'jun_total': jun_total,
    'jul_total': jul_total,
    'aug_total': aug_total,
    'sep_total': sep_total,
    'oct_total': oct_total,
    'nov_total': nov_total,
    'dec_total': dec_total,
    'q1_total': q1_total,
    'q2_total': q2_total,
    'q3_total': q3_total,
    'q4_total': q4_total,
    'sale_total': sale_total,
    }
    return render(request, 'Ledger/sale.html', context)

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
    return render(request, 'Ledger/form_budget.html', {'formset': formset, 'location': location})