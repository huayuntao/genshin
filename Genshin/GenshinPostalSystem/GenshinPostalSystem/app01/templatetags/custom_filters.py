# your_app/templatetags/custom_filters.py

from django import template

register = template.Library()


@register.filter(name='has_prefix')
def has_prefix(value, arg):
    """ 检查字符串是否以给定的前缀开头 """
    if isinstance(value, str) and isinstance(arg, str):
        return value.startswith(arg)
    return False
