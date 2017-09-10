from django import template
from django.core.urlresolvers import resolve

register = template.Library()


@register.simple_tag(takes_context=True)
def if_active_category(context, url_name, category):
    request = context['request']
    if category in request.path.split('/'):
        return 'active'
    return ''


@register.simple_tag(takes_context=True)
def highlight_if_active(context, url_name):
    request = context['request']
    match = resolve(request.path)
    if url_name == match.view_name:
        return 'active'
    return ''

