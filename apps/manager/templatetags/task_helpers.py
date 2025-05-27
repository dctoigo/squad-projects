from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def format_duration(duration):
    """
    Formata uma duração (timedelta) em formato mais legível
    Ex: 2h 30m
    """
    if not isinstance(duration, timedelta):
        return ""
    
    hours = duration.total_seconds() // 3600
    minutes = (duration.total_seconds() % 3600) // 60
    
    if hours == 0:
        return f"{int(minutes)}m"
    return f"{int(hours)}h {int(minutes)}m"

@register.filter
def timeuntil(duration, arg=None):
    """
    Formata uma duração em formato legível
    Ex: 2h 30min
    """
    if not isinstance(duration, timedelta):
        return ""
    
    hours = duration.total_seconds() // 3600
    minutes = (duration.total_seconds() % 3600) // 60
    
    if hours == 0:
        return f"{int(minutes)}min"
    return f"{int(hours)}h {int(minutes)}min"

@register.filter
def exclude_closed(tasks):
    if not tasks:
        return []
    if isinstance(tasks, str):
        return []
    return tasks.exclude(status='closed')

@register.filter
def only_closed(tasks):
    if not tasks:
        return []
    if isinstance(tasks, str):
        return []
    return tasks.filter(status='closed')

@register.filter
def as_field(field):
    """Renderiza um campo de formulário com label e mensagens de erro."""
    template = """
    <div class="form-group">
        <label class="form-label">{{ field.label }}</label>
        <div>{{ field }}</div>
        {% if field.errors %}
            <div class="invalid-feedback d-block">
                {{ field.errors|join:", " }}
            </div>
        {% endif %}
        {% if field.help_text %}
            <small class="form-text text-muted">{{ field.help_text }}</small>
        {% endif %}
    </div>
    """
    from django.template import Template, Context
    return Template(template).render(Context({'field': field}))