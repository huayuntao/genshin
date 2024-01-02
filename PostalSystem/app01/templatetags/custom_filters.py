
from django import template

register = template.Library()


@register.filter(name='has_prefix')
def has_prefix(value, arg):
    if isinstance(value, str) and isinstance(arg, str):
        return value.startswith(arg)
    return False
