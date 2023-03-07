from django.contrib import admin

# Register your models here.
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['street_address', 'city', 'state', 'zipcode']
    fields = ['street_address', 'street_address_2', 'city', 'state', 'zipcode', 'lat', 'lon']
    list_filter = ('state', )
    readonly_fields = ()
