from django import template
from contact.models import Social, About

register = template.Library()


@register.simple_tag()
def get_about():
    return About.objects.last()

@register.simple_tag()
def get_social_links():
    return Social.objects.all()

