from django import template
register = template.Library()

@register.filter
def custom(indexable, i):
    return indexable[i]