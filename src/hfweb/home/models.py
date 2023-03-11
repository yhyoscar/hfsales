from django.db import models
from django.utils.translation import ugettext_lazy

# Create your models here.


class ForTracker(models.Model):
    action = models.CharField(max_length=256, blank=True, null=True)
    tag  = models.CharField(max_length=256, blank=True, null=True)    
    meta = models.CharField(max_length=512, blank=True, null=True)
    
    def __str__(self):
        return self.tag + ' : ' + self.action

    class Meta:
        ordering = ['tag']
        verbose_name = "model for tracker"


class Feedback(models.Model):
    fullname = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(ugettext_lazy('email address'), blank=True, null=True)
    phone = models.CharField(max_length=256, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname + ' : ' + str(self.create_time)

    class Meta: 
        ordering = ['-create_time']

