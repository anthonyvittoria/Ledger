from django.shortcuts import render
from django.template import loader

from .models import Budget, Sale, Location

def index(request):
    return render(request, 'SalesQuery/index.html')

#################################################
########## BUDGET BY PLANT BY CUSTOMER ##########
#################################################

def cl_budget_plant_customer(request): # Choose location


    # create unique list of plant locations that have budgets recorded for them
    budget_locations = []
    for budget in Budget.objects.all():
        if budget.location not in budget_locations:
            budget_locations.append(budget.location)

    context = {
        'locations': budget_locations,
    }
    return render(request, 'SalesQuery/cl_budget_plant_customer.html', context)

def cy_budget_plant_customer(request, location_name_slug): # Choose year for budget by plant by customer
    
    years = []

    for budget in Budget.objects.filter(location__slug=location_name_slug):
        if budget.year not in years:
            years.append(budget.year)

    context = {
        'years': years,
        'location_name_slug': location_name_slug,
    }
    return render(request, 'SalesQuery/cy_budget_plant_customer.html', context)

def budget_plant_customer(request, location_name_slug, year): # Budget table view
    budget_objects = Budget.objects.filter(location__slug=location_name_slug, year=year)
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
    budget_total, cust_total = 0, 0

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
    return render(request, 'SalesQuery/budget_plant_customer.html', context)

###############################################
########## BUDGET BY PLANT BY SECTOR ##########
###############################################

def cl_budget_plant_sector(request): # Choose location

    budget_locations = []

    # create unique list of plant locations that have budgets recorded for them
    for budget in Budget.objects.all():
        if budget.location not in budget_locations:
            budget_locations.append(budget.location)

    context = {
        'locations': budget_locations
    }
    return render(request, 'SalesQuery/cl_budget_plant_sector.html', context)

def cy_budget_plant_sector(request, location_name_slug): # Choose year
    
    years = []

    for budget in Budget.objects.filter(location__slug=location_name_slug):
        if budget.year not in years:
            years.append(budget.year)

    context = {
        'years': years,
        'location_name_slug': location_name_slug,
    }
    return render(request, 'SalesQuery/cy_budget_plant_sector.html', context)

def budget_plant_sector(request, location_name_slug, year): # Budget table view

    # list of budgets corresponding to this plant and year
    budget_objects = Budget.objects.filter(location__slug=location_name_slug, year=year)
    
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
    'sector_data': sector_data,
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
    return render(request, 'SalesQuery/budget_plant_sector.html', context)

###############################################
########## BUDGET BY REGION BY PLANT ##########
###############################################

def cl_budget_region_plant(request): # Choose location
    
    regions = []
    for budget in Budget.objects.all():
        if budget.location.region not in regions:
            regions.append(budget.location.region)
    
    context = {
        'regions': regions,
    }
    return render(request, 'SalesQuery/cl_budget_region_plant.html', context)

def cy_budget_region_plant(request, region_name_slug): # Choose year
    
    years = []

    for budget in Budget.objects.filter(location__region__slug=region_name_slug):
        if budget.year not in years:
            years.append(budget.year)
    
    context = {
        'years': years,
        'region_name_slug': region_name_slug,
    }
    return render(request, 'SalesQuery/cy_budget_region_plant.html', context)

def budget_region_plant(request, region_name_slug, year): # Budget table view

    # list of budgets corresponding to this region and year
    budget_objects = Budget.objects.filter(location__region__slug=region_name_slug, year=year)

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
        'plant_data': plant_data,
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
    return render(request, 'SalesQuery/budget_region_plant.html', context)

##################################################
########## BUDGET BY REGION BY CUSTOMER ##########
##################################################

def cl_budget_region_customer(request): # Choose location
    regions = []
    for budget in Budget.objects.all():
        if budget.location.region not in regions:
            regions.append(budget.location.region)
    
    context = {
        'regions': regions,
    }
    return render(request, 'SalesQuery/cl_budget_region_customer.html', context)

def cy_budget_region_customer(request, region_name_slug): # Choose year

    years = []

    for budget in Budget.objects.filter(location__region__slug=region_name_slug):
        if budget.year not in years:
            years.append(budget.year)
    
    context = {
        'years': years,
        'region_name_slug': region_name_slug,
    }
    return render(request, 'SalesQuery/cy_budget_region_customer.html', context)

def budget_region_customer(request, region_name_slug, year):

    
    # list of budgets corresponding to this region and year
    budget_objects = Budget.objects.filter(location__region__slug=region_name_slug, year=year)

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
    'customer_data': customer_data,
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
    return render(request, 'SalesQuery/budget_region_customer.html', context)

################################################
########## BUDGET BY REGION BY SECTOR ##########
################################################

def cl_budget_region_sector(request): # Choose location

    regions = []
    for budget in Budget.objects.all():
        if budget.location.region not in regions:
            regions.append(budget.location.region)
    
    context = {
        'regions': regions,
    }
    return render(request, 'SalesQuery/cl_budget_region_sector.html', context)

def cy_budget_region_sector(request, region_name_slug): # Choose year

    years = []

    for budget in Budget.objects.filter(location__region__slug=region_name_slug):
        if budget.year not in years:
            years.append(budget.year)
    
    context = {
        'years': years,
        'region_name_slug': region_name_slug,
    }
    return render(request, 'SalesQuery/cy_budget_region_sector.html', context)

def budget_region_sector(request, region_name_slug, year): # Budget table view

    # list of budgets corresponding to this plant and year
    budget_objects = Budget.objects.filter(location__region__slug=region_name_slug, year=year)
    
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
    'sector_data': sector_data,
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
    return render(request, 'SalesQuery/budget_region_sector.html', context)