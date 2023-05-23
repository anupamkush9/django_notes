from django import template

from notes.models import Feedback

register = template.Library()

@register.simple_tag
def total_feedbacks():
    return Feedback.objects.count()

@register.simple_tag
def add_values(argument1, argument2, argument3):
    # Process the arguments or perform any other logic
    result = argument1 + argument2 + argument3
    return str(result)

