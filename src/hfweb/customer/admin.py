from django.contrib import admin

# Register your models here.
from .models import CustomerGroup, Customer
from django.utils.html import format_html
from django.utils.safestring import mark_safe

@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_customer_count', 'get_member_count']
    fields = ['name']
    list_filter = ()
    readonly_fields = ()

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'is_member', 'balance', 'group']
    fields = ['name', 'phone', 'group', 'address', 'email', 'wechat', 'facebook', 'is_member', 
        'membership_start_time', 'balance']
    list_filter = ('group', 'address__city', 'is_member')
    readonly_fields = ()


