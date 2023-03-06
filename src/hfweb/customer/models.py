from django.db import models
from commons.models import Address

# Create your models here.

class CustomerGroup(models.Model):
    name = models.CharField(max_length=20, verbose_name="客户分组名称")

    def __str__(self):
        return self.name

    def get_customer_count(self):
        return Customer.objects.filter(group__id=self.id).distinct().count()
    get_customer_count.short_description = "客户数量"

    def get_member_count(self):
        return Customer.objects.filter(group__id=self.id, is_member=True).distinct().count()
    get_member_count.short_description = "会员数量"


class Customer(models.Model):
    name = models.CharField(max_length=50, verbose_name="姓名")
    phone = models.CharField(max_length=10, verbose_name="电话")
    group = models.ForeignKey('CustomerGroup', on_delete=models.CASCADE, null=True, blank=True, verbose_name="分组")
    address = models.ForeignKey('Address', on_delete=models.CASCADE, null=True, blank=True, verbose_name="住址")
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name="Email")
    wechat = models.CharField(max_length=50, null=True, blank=True, verbose_name="微信")
    facebook = models.CharField(max_length=10, null=True, blank=True, verbose_name="Facebook")
    is_member = models.BooleanField(default=False, verbose_name="是否为禾富会员？")
    membership_start_time = models.DateTimeField(blank=True, null=True, verbose_name="注册会员时间")
    balance = models.FloatField(blank=True, null=True, verbose_name="账户余额")

    def __str__(self):
        if self.is_member:
            return f"{self.name}(会员)"
        else:
            return self.name

