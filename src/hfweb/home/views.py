import json
from django.core.checks import messages 
from django.shortcuts import render
from datetime import datetime
from .models import ForTracker, Feedback
from tracking_analyzer.models import Tracker
from django.http import JsonResponse
from django.conf import settings

from hfweb.settings import web_info
import glob
import os
import pandas as pd


surffixes = [ 'jpeg', 'jpg', 'png']
events_img = [f"/static/img/events/{os.path.basename(fn)}" for surffix in surffixes for fn in glob.glob(settings.STATIC_ROOT+'/img/events/*.'+surffix) if len(fn.split('.'))==2]
mem_imgs = sorted([f"/static/img/membership/{os.path.basename(fn)}" for surffix in surffixes for fn in glob.glob(settings.STATIC_ROOT+'/img/membership/*.'+surffix) if len(fn.split('.'))==2])
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

def homeview(request):
    Tracker.objects.create_from_request(request, 
        ForTracker.objects.get_or_create(action='view', tag='home', meta='{}')[0])

    if request.method == 'POST':
        if 'feedback' in request.POST:
            fb = Feedback.objects.create(fullname=request.POST.get('fullname', ''), 
                email=request.POST.get('email', ''), 
                phone=request.POST.get('phone', ''),                 
                message=request.POST.get('message', ''))
            Tracker.objects.create_from_request(request, fb)
            return render(request, 'thank_feedback.html', context = {'fullname': request.POST.get('fullname', ''), } )

        if 'click_logo' in request.POST:
            Tracker.objects.create_from_request(request, 
                ForTracker.objects.get_or_create(action='click logo', tag='logo', meta='{}')[0])
            return JsonResponse(dict())

        if 'click_menu' in request.POST:
            Tracker.objects.create_from_request(request, 
                ForTracker.objects.get_or_create(action='click menu', tag=request.POST['click_menu'], meta='{}')[0])
            return JsonResponse(dict())

        if 'click_button' in request.POST:
            Tracker.objects.create_from_request(request, 
                ForTracker.objects.get_or_create(action='click button', tag=request.POST['click_button'], meta='{}')[0])
            return JsonResponse(dict())

        if 'click_portfolio_box' in request.POST:
            Tracker.objects.create_from_request(request, 
                ForTracker.objects.get_or_create(action='click portfolio box', tag=request.POST['click_portfolio_box'], meta='{}')[0])
            return JsonResponse(dict())

    return render(request, 'home.html', 
        context = {'events_img': events_img, } )

def events_view(request):
    return render(request, 'events.html', {'oscar': 'test', } )

def membership_view(request):
    return render(request, 'membership.html', {'mem_imgs': mem_imgs, } )

def apply_membership_view(request):
    return render(request, 'apply_membership.html', {'states': states, 'product_options': product_options,
        'communications':communications, 'ships':ships, 'shoppings':shoppings, 'memtimes':memtimes} )

def contact_view(request):
    return render(request, 'contact.html', {'oscar': 'test', } )

def about_view(request):
    return render(request, "about.html", {'oscar': 'test'})



