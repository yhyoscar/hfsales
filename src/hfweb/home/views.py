import json
from django.core.checks import messages 
from django.shortcuts import render
from datetime import datetime
from .models import ForTracker, Feedback
from tracking_analyzer.models import Tracker
from django.http import JsonResponse

# Create your views here.


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
        context = {'oscar': 'hi oscar', } )
