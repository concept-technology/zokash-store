from django import template

register = template.Library()

@register.filter(name='to_int')
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0  # or you can return None or some other default value