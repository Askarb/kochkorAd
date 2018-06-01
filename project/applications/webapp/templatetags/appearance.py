from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import resolve

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


@register.simple_tag
def flag(code):
    if not isinstance(code, str):
        return code

    code = code.upper()
    return static(f'img/flags/{code}.svg')