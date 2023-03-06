from django.db import models
import pandas as pd
# Create your models here.

states = pd.read_csv('commons/states.csv')
states = zip(states['code'].values, states['state'].values)

class Address(models.Model):
    street_address   = models.CharField(max_length=50, blank=True, null=True, verbose_name="Street")
    street_address_2 = models.CharField(max_length=50, blank=True, null=True, default="")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="City")
    state = models.CharField(max_length=2, default="NY", choices=states, blank=True, null=True, verbose_name="State")
    zipcode = models.CharField(max_length=5, blank=True, null=True, verbose_name='ZIP')
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    def __str__(self):
        street = f"{self.street_address}"
        if self.street_address_2: street += f", {self.street_address_2}"
        return f"{street}, {self.city}, {self.state} {self.zipcode}"


class Transaction(models.Model):
    time = models.DateTimeField(auto_now_add=True, verbose_name="付款时间")
    method = models.CharField(max_length=2, verbose_name="付款方式",
        choices=[("CS", "现金"),
                 ("CK", "支票"),
                 ("ZE", "zelle转账"),
                 ("VM", "venmo转账"),
                 ("CC", "信用卡"),
                 ("OT", "其它")])
    amount = models.FloatField(verbose_name="金额($)")
    memo = models.CharField(max_length=50, null=True, blank=True, verbose_name="备注")

    def __str__(self):
        return f"{self.time}: {self.method} ${round(self.amount,2)}"
