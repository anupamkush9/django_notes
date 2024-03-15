from django import template

register = template.Library()

@register.filter
def add_two_num(value, number1):
    return value + number1

@register.filter
def display_first_char(value):
    return value[0]