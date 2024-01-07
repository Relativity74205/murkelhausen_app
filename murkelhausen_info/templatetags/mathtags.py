from django import template

register = template.Library()


@register.filter
def multiply(value, factor, *args, **kwargs):
    return value * factor


@register.filter
def normalize(value, factor, *args, **kwargs):
    return value / factor
