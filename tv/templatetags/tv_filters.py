
from django import template

register = template.Library()

@register.filter
def name(imageHolder):
    return imageHolder.filename

@register.filter
def path(imageHolder):
    return imageHolder.path
