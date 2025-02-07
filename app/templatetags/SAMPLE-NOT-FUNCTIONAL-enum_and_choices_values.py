from django import template

import copy

register = template.Library()

@register.simple_tag
def get_text_choice_display(name, index, enum):    
    """
    SAMPLE TAG CODE - NOT FUNCTIONAL !!
    
    Returns the correspding value from an enum tuple or list value

    Args:
        name (Enum item name, or models.TextChoices value)
        index (int): index of the value in the tuple value
        enum (Enum): the actual enum

    Returns:
        mutable: The value

    Usage:
        In the view, pass the corresponding string list to template.
        - Load
        - Use like this in template:

        ```html
            {% load enum_values %}

            {% get_enum_tuple_value trainingcoursesession.preparation 1 TaskStatus %}
    """
    for name, value in enum.choices:
        print(name, value)
        if str(name) == str(enum_value):
            return value[index]

