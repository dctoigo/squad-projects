from django import template
from django.utils.timesince import timesince
from django.utils import timezone

register = template.Library()

@register.filter
def smart_timesince(value):
    """Retorna tempo de forma mais inteligente"""
    if not value:
        return ""
    
    now = timezone.now()
    diff = now - value
    
    if diff.days > 7:
        return value.strftime("%d/%m/%Y")
    elif diff.days > 0:
        return f"{diff.days} dia{'s' if diff.days > 1 else ''} atrás"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hora{'s' if hours > 1 else ''} atrás"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minuto{'s' if minutes > 1 else ''} atrás"
    else:
        return "Agora mesmo"

@register.filter
def percentage(value, total):
    """Calcula porcentagem"""
    if not total or total == 0:
        return 0
    return round((value / total) * 100)