from django import template

register = template.Library()


@register.filter
def percentage(value1, value2=100):
    return int(value1) / int(value2) * 100
