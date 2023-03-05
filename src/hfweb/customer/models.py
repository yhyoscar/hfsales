from django.db import models

# Create your models here.


class CustomerGroup(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_customer_count(self):
        return Customer.objects.filter(group__id=self.id).distinct().count()

    def get_member_count(self):
        return Customer.objects.filter(group__id=self.id, is_member=True).distinct().count()


class Address(models.Model):
    street_address   = models.CharField(max_length=50)
    street_address_2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2, default="NY")
    zip = models.CharField(max_length=5)
    distance_from_farm = models.FloatField(verbose_name="到禾富农场的距离（单位：mile）", blank=True, null=True)
    group = models.CharField(max_length=50, verbose_name="地址分组", blank=True, null=True)


class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    group = models.ForeignKey('CustomerGroup', on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, null=True, blank=True)
    pickup_address = models.ForeignKey('Address', on_delete=models.CASCADE, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    wechat = models.CharField(max_length=50, null=True, blank=True)
    facebook = models.CharField(max_length=10, null=True, blank=True)
    is_member = models.BooleanField(default=False, verbose_name="是否为禾富会员？")
    membership_start_time = models.DateTimeField(blank=True, null=True, verbose_name="注册会员时间")
    balance = models.FloatField(blank=True, null=True, verbose_name="账户余额")


