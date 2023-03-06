from django.contrib import admin

# Register your models here.
from .models import Group, Customer, Transaction
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
    list_display = ['name', 'is_member', 'show_balance', 'phone', 'group']
    fields = ['name', 'is_member', 'membership_start_time',
            'show_balance', 'show_deposit_info', 'show_consume_info',
            'group', 'street_address', 'city', 'state', 'zipcode',
            'phone', 'email', 'wechat', 'facebook', ]
    list_filter = ('group', 'is_member')
    readonly_fields = ('show_balance', 'show_deposit_info', 'show_consume_info')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['time', 'customer', 'purpose', 'amount', 'method']
    fields = ['time', 'customer', 'purpose', 'amount', 'method', 'memo']
    list_filter = ('customer', 'purpose', 'method')
    readonly_fields = ()

