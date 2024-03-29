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
    list_display = ['name', 'is_member', 'show_balance', 'trans_button', 'show_prefer_communication', 'group']
    list_filter = ('group', 'is_member')
    readonly_fields = ('show_balance', 'show_deposit_info', 'show_consume_info', 'show_transaction_history')
    fieldsets = [
        (None, {
            'fields': ('name', 'group', 'is_member', 'create_time', 'membership_start_time', 'show_balance')
        }),
        ('交易记录', {
        'fields': ['show_deposit_info', 'show_consume_info', 'show_transaction_history'],
        'classes': ['collapse',]
        }),
        ('联系方式', {
        'fields': ['street_address', 'city', 'state', 'zipcode',
            'phone', 'email', 'wechat', 'facebook','bak_name', 'bak_phone',],
        'classes': ['collapse',]
        }),
        ('个人偏好', {
        'fields': ['prefer_communication',
            ('prefer_product_1', 'prefer_product_2', 'prefer_product_3'),
            'prefer_shopping', 'prefer_ship', 'prefer_membership',],
        'classes': ['collapse',]
        }),
        (None, {
            'fields': ('note',)
        }),
    ]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['time', 'customer_link', 'method', 'amount', 'payfor']
    fields = ['time', 'customer', 'method', 'amount', 'payfor', 'memo']
    list_filter = ('customer', 'method', 'payfor')
    readonly_fields = ()

    def customer_link(self, obj):
        return mark_safe(f'<a href="/admin/customer/customer/{obj.customer.id}/change/">{obj.customer.__str__()}</a>')
    customer_link.short_description = "付款人"
    customer_link.allow_tags = True

    class Media:
        js = ["admin/js/transaction_form.js"]

