from django import template
register = template.Library()

@register.simple_tag
def define(val=None):
  """
    @description
      Usage
      -----

      ```django
      {% load define_action %}
      {% if item %}

         {% define "Edit" as action %}

      {% else %}

         {% define "Create" as action %}

      {% endif %}      
      ```

      Src
      ---
      https://stackoverflow.com/questions/1070398/how-to-set-a-value-of-a-variable-inside-a-template-code#answer-37755722
  """
  return val