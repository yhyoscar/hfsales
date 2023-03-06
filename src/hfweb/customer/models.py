from django.db import models
from commons.models import Address, Transaction

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=20, verbose_name="客户分组名称")

    def __str__(self):
        return self.name

    def get_customer_count(self):
        return Customer.objects.filter(group__id=self.id).distinct().count()
    get_customer_count.short_description = "客户数量"

    def get_member_count(self):
        return Customer.objects.filter(group__id=self.id, is_member=True).distinct().count()
    get_member_count.short_description = "会员数量"


class Customer(Address):
    name = models.CharField(max_length=50, verbose_name="姓名")
    phone = models.CharField(max_length=10, null=True, blank=True, verbose_name="电话")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True, verbose_name="分组")
    #address = models.ForeignKey('Address', on_delete=models.CASCADE, null=True, blank=True, related_name="address", verbose_name="住址")
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name="Email")
    wechat = models.CharField(max_length=50, null=True, blank=True, verbose_name="微信")
    facebook = models.CharField(max_length=10, null=True, blank=True, verbose_name="Facebook")
    is_member = models.BooleanField(default=False, verbose_name="是否为禾富会员？")
    membership_start_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="成为会员时间")
    #balance = models.FloatField(default=0.0, verbose_name="账户余额")
    #deposit_history = models.ManyToManyField("Transaction", null=True, blank=True, verbose_name="充值记录")

    def __str__(self):
        if self.is_member:
            return f"{self.name}(会员)"
        else:
            return self.name
    
    def get_balance(self):
        balance = 0.0
        for obj in Transaction.objects.filter(customer__id=self.id):
            balance += obj.purpose * obj.amount
        return balance

    def show_balance(self):
        return f"${round(self.get_balance(), 2)}"

    def get_deposit_info(self):
        total = 0.0
        objs = Transaction.objects.filter(customer__id=self.id, purpose>0)
        for obj in objs:
            total += obj.amount
        return len(objs), total

    def show_deposit_info(self):
        n, s = self.get_deposit_info()
        return f"充值{n}次，总共${round(s, 2)}"

    def get_consume_info(self):
        total = 0.0
        objs = Transaction.objects.filter(customer__id=self.id, purpose<0)
        for obj in objs:
            total += obj.amount
        return len(objs), total

    def show_consume_info(self):
        n, s = self.get_consume_info()
        return f"消费{n}次，总共${round(s, 2)}"


class Transaction(models.Model):
    customer = models.ForeignKey("Customer", verbose_name="付款人")
    time = models.DateTimeField(auto_now_add=True, verbose_name="付款时间")
    method = models.CharField(max_length=2, verbose_name="付款方式",
        choices=[("CS", "现金"),
                 ("CK", "支票"),
                 ("ZE", "zelle转账"),
                 ("VM", "venmo转账"),
                 ("CC", "信用卡"),
                 ("OT", "其它")])
    amount = models.FloatField(verbose_name="金额($)")
    purpose = models.IntegerField(verbose_name="付款目的", 
        choices=[(1, "充值"), (-1, "消费")])
    memo = models.CharField(max_length=50, null=True, blank=True, verbose_name="备注")

    def __str__(self):
        return f"{self.time}: {self.customer} {self.get_purpose_display()}${round(self.amount,2)}"
