from django.db import models
import pandas as pd
from hfweb.settings import web_info

# Create your models here.


states = pd.read_csv(web_info['states_csv_path'])
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
