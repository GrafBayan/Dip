from django import template
from django.apps import apps

register = template.Library()

@register.filter
def instanceof(value, klass_name):
    try:
        klass = apps.get_model(klass_name)  #'MyChat.ChatInvite'
        return isinstance(value, klass)
    except LookupError:
        return False