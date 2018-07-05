from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()


@register.filter
def split(func):
    return func.__class__.__name__


@register.filter
@stringfilter
def cut(value, arg):
    return value.replace(arg, '')