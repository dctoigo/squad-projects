from django import template
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()

@register.simple_tag
def logo_exists(path='img/logo.png'):
    return staticfiles_storage.exists(path)