from django import template
register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None