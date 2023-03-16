from django.contrib import admin

# Register your models here.
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'show_unit_price', 'show_retail_unit_price', 'show_storage', "unit_note", 'need_refrig', 'need_freeze']
    fields = ['name', 'category', 'picture', 'show_picture', 'description', 
            'unit', 'unit_note', 'unit_price', 'retail_unit_price', 'number_in_stock',
            'need_refrig', 'need_freeze']
    list_filter = ('category', 'need_refrig', 'need_freeze')
    readonly_fields = ("show_picture", )


