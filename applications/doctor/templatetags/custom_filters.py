from django import template

register = template.Library()

@register.filter
def split(value, key):
    """Divide un string por el separador key"""
    return value.split(key)
