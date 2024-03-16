from django import template

register = template.Library()

@register.simple_tag
def is_thing(is_component_thing, id):
    return is_component_thing.get(id)
