from django.contrib import admin

from .models import Profile, Posts

'''class ProfileAdmin(admin.ModelAdmin):
    pass'''
admin.site.register(Profile)
admin.site.register(Posts)
