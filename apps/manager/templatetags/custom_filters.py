from django import template

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