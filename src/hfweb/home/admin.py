from django.contrib import admin

# Register your models here.
from .models import ForTracker, Feedback

@admin.register(ForTracker)
class ForTrackerAdmin(admin.ModelAdmin):
    list_display = ('action', 'tag', 'meta')
    fields = ['action', 'tag', 'meta']
    list_filter = ['tag']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'fullname', 'email', 'phone')
    fields = ['create_time', 'fullname', 'email', 'phone', 'message']
    list_filter = ['email']
    readonly_fields = ['create_time']
