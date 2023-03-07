from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="产品名称")
    category = models.CharField(max_length=2, verbose_name="产品类别",
        choices=[('MR', '食用菌'),
                 ('VG', '蔬菜'),
                 ('FR', '瓜果'),
                 ('EG', '蛋类'),
                 ('MT', '肉类'),
                 ('CK', '熟食'),
                 ('OT', '其它')])
    description = models.TextField(max_length=500, verbose_name="产品介绍", null=True, blank=True)
    picture = models.ImageField(verbose_name="产品图片", null=True, blank=True)
    unit = models.CharField(max_length=2, verbose_name="单位", null=True, blank=True,
        choices=[('G', '个'),
                 ('Z', '只'),
                 #('H', '半只'),
                 ('12', '打（12个）'),
                 ('lb', '磅'),
                 ('oz', '盎司')])
    unit_price = models.FloatField(verbose_name="单价", null=True, blank=True)
    number_in_stock = models.FloatField(verbose_name="现有存货数量", null=True, blank=True)
    need_refrig = models.BooleanField(default=False, verbose_name="需要冷藏")
    need_freeze = models.BooleanField(default=False, verbose_name="需要冷冻")

    def __str__(self):
        return self.name

    def show_storage(self):
        return f"{self.number_in_stock} {self.get_unit_display()}"
    show_storage.short_description = "存货数量"

    
