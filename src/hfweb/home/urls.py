from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeview, name='home'), 
    path('events/', views.events_view, name="events"),
    path('membership/', views.membership_view, name="membership"),
    path('contact/', views.contact_view, name="contact"),
    path('about/', views.about_view, name="about"),
    #path('apply-membership', views.apply_membership_view, name="apply_membership"),
]
