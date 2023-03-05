from django.contrib import admin

# Register your models here.
from .models import CustomerGroup, Address, Customer
from django.utils.html import format_html
from django.utils.safestring import mark_safe

@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ['name']
    list_filter = ()
    readonly_fields = ()

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['street_address', 'city', 'state', 'zip', 'distance_from_farm', 'group']
    fields = [('street_address', 'street_address_2', 'city', 'state', 'zip'), 'distance_from_farm', 'group']
    list_filter = ('city', 'state', 'group')
    readonly_fields = ()

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'is_member', 'balance', 'group']
    fields = ['name', 'phone', 'group', 'address', 'pickup_address', 'email', 'wechat', 'facebook', 'is_member', 
        'membership_start_time', 'balance']
    list_filter = ('group', 'pickup_address', 'is_member')
    readonly_fields = ()


