from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()


@register.filter
@stringfilter
def replace(value, arg):
    return value.replace(arg, '')