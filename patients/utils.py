from django.shortcuts import redirect
from core.models import Patient

def get_patinet_or_redirect(request, redirect_url_name):
    try:
        return request.user.patient
    except Patient.DoesNotExist:
        return redirect(redirect_url_name)