# templatetags/roles.py

from django import template

register = template.Library()


@register.filter
def is_doctor(user):
    return hasattr(user, "doctor")


@register.filter
def is_patient(user):
    return hasattr(user, "patient")