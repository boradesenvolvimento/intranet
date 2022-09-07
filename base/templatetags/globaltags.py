
from django import template
from django.contrib.auth.models import User

from base import models
from django.utils.functional import SimpleLazyObject
register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.simple_tag
def profileuser(obj):
    usuario = models.Profile.objects.get(username=obj)
    return usuario

@register.filter
def parse_string(obj):
    return str(obj)

