from django.contrib import admin

# Register your models here.
from .models import Address, Transaction

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['street_address', 'city', 'state', 'zipcode']
    fields = ['street_address', 'street_address_2', 'city', 'state', 'zipcode', 'lat', 'lon']
    list_filter = ('state')
    readonly_fields = ()

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['time', 'amount', 'method']
    fields = ['time', 'amount', 'method', 'memo']
    list_filter = ('method')
    readonly_fields = ()


