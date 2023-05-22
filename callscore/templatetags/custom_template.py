from django import template

register = template.Library()
@register.filter
def get_item(list, index):
    try:
        return list[index]
    except:
        return None

@register.filter
def get_length(iterable):
    return len(iterable)