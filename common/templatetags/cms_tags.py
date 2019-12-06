from urllib.parse import urlencode
from django import template

register = template.Library()

# copied from https://stackoverflow.com/a/36288962/369018
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
