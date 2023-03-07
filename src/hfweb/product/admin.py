from django.contrib import admin

# Register your models here.
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_category_display', 'show_storage', 'need_refrig', 'need_freeze']
    fields = ['name', 'category', 'picture', 'description', 'unit', 'unit_price', 'number_in_stock',
        'need_refrig', 'need_freeze']
    list_filter = ('category', 'need_refrig', 'need_freeze')
    readonly_fields = ()
