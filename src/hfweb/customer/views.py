import json
from django.core.checks import messages
from django.shortcuts import render
from datetime import datetime
from .models import Customer
from home.models import ForTracker
from tracking_analyzer.models import Tracker
from django.http import JsonResponse
from django.conf import settings

from hfweb.settings import web_info
import glob
import os
import pandas as pd

# Create your views here.

states = pd.read_csv(web_info['states_csv_path'])
states = dict(zip(states['code'].values, states['state'].values))
product_options = [ ('MR', '食用菌', 'Mushroom'),
                        ('VG', '蔬菜', 'Vegetable'),
                        ('FR', '瓜果', 'Squash/Fruit'),
                        ('EG', '蛋类', 'Eggs'),
                        ('MT', '肉类', 'Meat'),
                        ('CK', '熟食', 'Prepared Food')]
product_options = {x:z for x,y,z in product_options}
communications = {'E':'Email', 'P': 'Phone Call', 'T':'Text Message', 'C': 'Wechat'}
shoppings = {'W':'Online', 'P':'Phone', 'C':'Wechat'}
ships = {'D': 'Deliver to my address', 'L': 'Local pickup site', 'F': 'Pickup at the farm'}
memtimes = {'A': 'as soon as possible',
            '1': 'in the next one month',
            '3': 'in the next 3 months',
            'Y': 'in the next 12 months',
            'N': 'never'}


def apply_membership_view(request):
    Tracker.objects.create_from_request(request,
        ForTracker.objects.get_or_create(action='view', tag='customer/apply_membership', meta='{}')[0])
    if request.method == 'POST':
        if 'apply_membership' in request.POST:
            fb = Customer.objects.create(create_time=datetime.now(),
                name=request.POST.get('fullname', ''),
                email=request.POST.get('email', ''),
                phone=request.POST.get('phone', ''),
                street_address=request.POST.get('street', ''),
                city=request.POST.get('city', ''),
                state=request.POST.get('state', ''),
                zipcode=request.POST.get('zip', ''),
                wechat=request.POST.get('wechat', ''),
                bak_name=request.POST.get('emergency_name', ''),
                bak_phone=request.POST.get('emergency_phone', ''),
                prefer_communication=request.POST.get('prefer_communication', ''),
                prefer_product_1=request.POST.get('prefer_product_1', ''),
                prefer_product_2=request.POST.get('prefer_product_2', ''),
                prefer_product_3=request.POST.get('prefer_product_3', ''),
                prefer_shopping=request.POST.get('prefer_shopping', ''),
                prefer_ship=request.POST.get('prefer_ship', ''),
                prefer_membership=request.POST.get('prefer_memtime', ''),
                note=request.POST.get('message', ''))
            Tracker.objects.create_from_request(request, fb)
            return render(request, 'thank_apply_membership.html', context = {'fullname': request.POST.get('fullname', ''), } )

    
    return render(request, 'apply_membership.html', {'states': states, 'product_options': product_options,
        'communications':communications, 'ships':ships, 'shoppings':shoppings, 'memtimes':memtimes} )



