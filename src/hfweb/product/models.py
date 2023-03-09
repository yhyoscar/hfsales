from django.db import models

# Create your models here.
from django.utils.html import escape
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="产品名称")
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
                 ('H', '份(每份半只)'),
                 ('B', '袋(每袋50个)'),
                 ('12', '打(每打12个)'),
                 ('lb', '磅'),
                 ('oz', '盎司')])
    #unit_note = models.CharField(max_length=20, verbose_name="单位备注", null=True, blank=True)
    unit_price = models.FloatField(verbose_name="单价($)", null=True, blank=True)
    number_in_stock = models.FloatField(verbose_name="库存数量", null=True, blank=True)
    need_refrig = models.BooleanField(default=False, verbose_name="需要冷藏")
    need_freeze = models.BooleanField(default=False, verbose_name="需要冷冻")

    def __str__(self):
        return self.name

    def show_storage(self):
        if self.number_in_stock > 0:
            out = f'<b><font color="green">{self.number_in_stock}</font></b>'
        else:
            out = f'<b><font color="red">{self.number_in_stock}</font></b>'
        out = f"{out} {self.get_unit_display()}"
        if hasattr(self, "unit_note"):
            if self.unit_note:
                out += f"({self.unit_note})"
        return mark_safe(out)
    show_storage.short_description = "库存数量"

    def show_picture(self):
        return mark_safe(u'<img src="%s" ' % escape(self.picture.url) + 'style="max-width: 100%;">')
    show_picture.short_description = '产品图片'
    show_picture.allow_tags = True    
