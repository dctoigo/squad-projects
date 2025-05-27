from django import template
from django.utils.safestring import mark_safe
from django.forms.boundfield import BoundField
from django.forms.widgets import (
    CheckboxInput, Select, SelectMultiple, RadioSelect
)

from datetime import timedelta

register = template.Library()

@register.simple_tag
def render_field(field: BoundField):
    """
    Renderiza automaticamente o campo com classes Bootstrap:
    - form-control (default)
    - form-select (selects)
    - form-check-input (checkboxes)
    """
    widget = field.field.widget
    errors = ''.join(f'<div class="invalid-feedback">{e}</div>' for e in field.errors)
    is_invalid = ' is-invalid' if field.errors else ''

    # CHECKBOXES
    if isinstance(widget, CheckboxInput):
        html = f"""
        <div class="form-check mb-3">
          {field.as_widget(attrs={'class': 'form-check-input' + is_invalid})}
          <label class="form-check-label" for="{field.id_for_label}">{field.label}</label>
          {errors}
        </div>
        """

    # SELECTS (drop-downs ou múltiplas escolhas)
    elif isinstance(widget, (Select, SelectMultiple, RadioSelect)):
        attrs = {'class': 'form-select' + is_invalid}
        label = f'<label for="{field.id_for_label}" class="form-label">{field.label}</label>'
        html = f"""
        <div class="mb-3">
          {label}
          {field.as_widget(attrs=attrs)}
          {errors}
        </div>
        """

    # OUTROS CAMPOS (texto, data, número, email etc.)
    else:
        attrs = {'class': 'form-control' + is_invalid}
        # Preserva type se definido no widget original
        widget_attrs = getattr(widget, 'attrs', {})
        if 'type' in widget_attrs:
            attrs['type'] = widget_attrs['type']
        elif hasattr(widget, 'input_type'):
            attrs['type'] = widget.input_type

        label = f'<label for="{field.id_for_label}" class="form-label">{field.label}</label>'
        html = f"""
        <div class="mb-3">
          {label}
          {field.as_widget(attrs=attrs)}
          {errors}
        </div>
        """

    return mark_safe(html)

@register.filter
def is_multiple(field):
    from django.forms.widgets import SelectMultiple
    return isinstance(field.field.widget, SelectMultiple)

@register.filter
def split(value, delimiter=','):
    return value.split(delimiter)

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})

