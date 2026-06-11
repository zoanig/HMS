from django.shortcuts import redirect
from core.models import Patient, Appointment
from django.utils import timezone
from datetime import datetime, timedelta


def get_patinet_or_redirect(request, redirect_url_name):
    try:
        return request.user.patient
    except Patient.DoesNotExist:
        return redirect(redirect_url_name)
    
def generate_slots(date):
    START_HOUR = 9
    END_HOUR = 17
    SLOT_DURATION = timedelta(minutes=30)
    start = datetime.combine(
        date,
        datetime.min.time()
    ).replace(hour=START_HOUR)

    end = start.replace(hour=END_HOUR)

    slots = []

    while start < end:
        slots.append(start.time())
        start += SLOT_DURATION

    return slots