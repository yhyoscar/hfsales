from django.db import models
import pandas as pd

# Create your models here.

states = pd.read_csv('customer/states.csv')
states = zip(states['code'].values, states['state'].values)

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


class Address(models.Model):
    street_address   = models.CharField(max_length=50)
    street_address_2 = models.CharField(max_length=50, blank=True, null=True, default="")
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2, default="NY", choices=states)
    zip = models.CharField(max_length=5)
    distance_from_farm = models.FloatField(verbose_name="到农场距离(mile)", blank=True, null=True)
    is_pickup = models.BooleanField(default=False, verbose_name="是否为取货点?", blank=True, null=True)

    def __str__(self):
        out = ""
        if self.is_pickup: out += "[取货点] "
        out += f"{self.street_address}"
        if self.street_address_2: out += f", {self.street_address_2}"
        return f"{out}, {self.city}, {self.state} {self.zip}"
        


class Customer(models.Model):
    name = models.CharField(max_length=50, verbose_name="姓名")
    phone = models.CharField(max_length=10, verbose_name="电话")
    group = models.ForeignKey('CustomerGroup', on_delete=models.CASCADE, null=True, blank=True, verbose_name="客户分组")
    address = models.ForeignKey('Address', on_delete=models.CASCADE, null=True, blank=True, related_name="address", verbose_name="住址")
    pickup_address = models.ForeignKey('Address', on_delete=models.CASCADE, null=True, blank=True, related_name="pickup_address", verbose_name="取货地址")
    email = models.CharField(max_length=50, null=True, blank=True)
    wechat = models.CharField(max_length=50, null=True, blank=True, verbose_name="微信")
    facebook = models.CharField(max_length=10, null=True, blank=True)
    is_member = models.BooleanField(default=False, verbose_name="是否为禾富会员？")
    membership_start_time = models.DateTimeField(blank=True, null=True, verbose_name="注册会员时间")
    balance = models.FloatField(blank=True, null=True, verbose_name="账户余额")

    def __str__(self):
        return self.name

