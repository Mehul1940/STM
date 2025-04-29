from django import template

register = template.Library()

@register.filter
def get_attr(obj, field):
    return getattr(obj, field)