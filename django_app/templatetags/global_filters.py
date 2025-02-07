from django import template

register = template.Library()

@register.filter()
def field_name_to_label(value):
    """
        Error: Invalid filter: 'field_name_to_label' !!
    """
    value = value.replace('_', ' ')
    return value.title()
