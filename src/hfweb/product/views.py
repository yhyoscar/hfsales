from django.shortcuts import render
from .models import Product
# Create your views here.

categories = [('MR', 'Mushroom', '蘑菇'),
             ('VG', 'Vegetable', '蔬菜'),
             ('FR', 'Squash / Fruit', '瓜果'),
             ('MG', 'Microgreens', '芽菜'),
             ('EG', 'Eggs', '蛋类'),
             ('MT', 'Meat', '肉类'),
             ('CK', 'Prepared Food', '熟食'),
             ('OT', 'Others', '其它')]

units = [('G', '个', 'each'),
         ('Z', '只', 'each'),
         ('H', '份', 'serve'),
         ('B', '袋', 'bag'),
         ('12', '打', 'dozen'),
         ('lb', '磅', 'lb'),
         ('oz', '盎司', 'oz')]
units = {x:z for x,y,z in units}

def products_view(request):
    prods = dict()
    for x,y,z in categories:
        objs = Product.objects.filter(category=x).distinct()
        if objs.count() > 0:
            for obj in objs:
                obj.unit_en = units[obj.unit]
            prods[f"{y} ({z})"] = objs
    return render(request, 'products.html', {'products': prods, } )


