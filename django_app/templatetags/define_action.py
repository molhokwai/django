from django import template
register=template.Library()
@register.simple_tag
def define(val=None):'\n    @description\n      Usage\n      -----\n\n      ```django\n      {% load define_action %}\n      {% if item %}\n\n         {% define "Edit" as action %}\n\n      {% else %}\n\n         {% define "Create" as action %}\n\n      {% endif %}      \n      ```\n\n      Src\n      ---\n      https://stackoverflow.com/questions/1070398/how-to-set-a-value-of-a-variable-inside-a-template-code#answer-37755722\n  ';return val