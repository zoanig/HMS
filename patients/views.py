from django.shortcuts import render, redirect
from core.models import Patient, Appointment, Billing, PrescriptionMedication
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .utils import get_patinet_or_redirect
import humanize
from django.utils import timezone

# Create your views here.
@login_required
def dashboard(request):
    patient = get_patinet_or_redirect(request, "core:index")
    if not isinstance(patient, Patient):
        return patient
    appointments = patient.appointment_set.order_by('-appointment_date')
    total_appointments = len(appointments)
    billings = Billing.objects.filter(patient = patient.id)[:1]
    pms = PrescriptionMedication.objects.filter(prescription__patient = patient.id)
    ongoing_pms = []
    for pm in pms:
        if pm.status == "Ongoing":
            ongoing_pms.append(pm)
    latest_prescription = patient.prescription_set.order_by('-created_at').first()
    context = {"appointments": appointments[:2], "billings": billings, "pms": ongoing_pms, "latest_prescription": latest_prescription, "total_appointments": total_appointments}
    return render(request, "dashboard.html", context)

@login_required
def get_appointment(request, pk):
    patient = get_patinet_or_redirect(request, "core:index")
    if not isinstance(patient, Patient):
        return patient
    apt = ""
    try:
        apt = patient.appointment_set.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, "core/404.html", {"message": "The resource you are trying to access doesnt. Or you're unauthorized to access it"})
    difference = ""
    if apt.appointment_date > timezone.now():
        difference = apt.appointment_date - timezone.now()
    else:
        difference = timezone.now() - apt.appointment_date
    time =  humanize.naturaltime(difference)
    context = {"apt": apt, "time": apt.status + " " + time}
    return render(request, "appointment.html", context)

@login_required
def appointments_history(request):
    patient = get_patinet_or_redirect(request, "core:index")
    if not isinstance(patient, Patient):
        return patient
    appointments = patient.appointment_set.order_by('-appointment_date')
    context = {"appointments": appointments}
    return render(request, "appointment_history.html", context)

@login_required
def prescription_history(request):
    patient = get_patinet_or_redirect(request, "core:index")
    if not isinstance(patient, Patient):
        return patient
    prescriptions = patient.prescription_set.all().order_by('-created_at')
    context = {"prescriptions": prescriptions}
    return render(request, "prescriptions_history.html", context)
    
def prescription_detail(request, pk):
    patient = get_patinet_or_redirect(request, "core:index")
    if not isinstance(patient, Patient):
        return patient
    presc = ""
    try:
        presc = patient.prescription_set.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, "core/404.html", {"message": "The resource you are trying to access doesnt. Or you're unauthorized to access it"})
    context = {"presc": presc}
    return render(request, "presc_detail.html", context)

@login_required
def medication_history(request):
    patient = get_patinet_or_redirect(request, "core:index")
    if not isinstance(patient, Patient):
        return patient
    pms = PrescriptionMedication.objects.filter(prescription__patient = patient.id).order_by('-prescription__created_at')
    context = {"pms": pms}
    return render(request, "medications_history.html", context)
