from django.contrib import admin

# Register your models here.
from .models import Group, Customer
from django.utils.html import format_html
from django.utils.safestring import mark_safe

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_customer_count', 'get_member_count']
    fields = ['name']
    list_filter = ()
    readonly_fields = ()

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_member', 'balance', 'phone', 'group']
    fields = ['name', 'group', 'street_address', 'city', 'state', 'zipcode',
            'phone', 'email', 'wechat', 'facebook', 'is_member', 'membership_start_time', 'balance']
    list_filter = ('group', 'is_member')
    readonly_fields = ()


