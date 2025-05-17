from django import template

register = template.Library()

@register.filter
def not_in(value, exclude_csv):
    exclude_list = [item.strip() for item in exclude_csv.split(',')]
    return value not in exclude_list