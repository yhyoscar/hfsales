from django.urls import path
from . import views

urlpatterns = [
    path('apply-membership', views.apply_membership_view, name="apply_membership"),
]
