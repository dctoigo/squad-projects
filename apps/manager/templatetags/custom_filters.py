from django import template
from django.conf import settings
from django.contrib.staticfiles.finders import find


register = template.Library()

@register.filter
def not_in(value, exclude_csv):
    exclude_list = [item.strip() for item in exclude_csv.split(',')]
    return value not in exclude_list


@register.filter
def startswith(value, arg):
    """Retorna True se 'value' começa com 'arg'."""
    if isinstance(value, str) and isinstance(arg, str):
        return value.startswith(arg)
    return False

@register.filter
def to_range(start, end):
    return range(start, end)

@register.filter
def file_exists(filepath):
    """Verifica se um arquivo estático existe"""
    try:
        # Procurar o arquivo nos diretórios estáticos
        found_file = find(filepath)
        return found_file is not None
    except:
        return False

@register.simple_tag
def static_exists(filepath):
    """Template tag para verificar se arquivo estático existe"""
    try:
        found_file = find(filepath)
        return found_file is not None
    except:
        return False