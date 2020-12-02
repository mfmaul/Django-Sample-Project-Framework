import uuid
from django import template

register = template.Library()

@register.simple_tag
def Guid():
    return str(uuid.uuid4())