from django import template
register=template.Library()
@register.filter()
def field_name_to_label(value):"\n        Error: Invalid filter: 'field_name_to_label' !!\n    ";A=value;A=A.replace('_',' ');return A.title()