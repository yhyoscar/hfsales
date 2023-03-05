from django.db import models

# Create your models here.


class CustomerGroup(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_customer_count():
        return Customer.objects.filter(group__id=self.id).distinct().count()

    def get_member_count():
        return Customer.objects.filter(group__id=self.id, is_member=True).distinct().count()


class Customer(models.Model):
    name = models.CharField(max_length=50)
    is_member = models.BooleanField(default=False, verbose_name="Is a member of Hephzibah farm?")
    membership_start_time = models.DateTimeField(blank=True, null=True)
     
