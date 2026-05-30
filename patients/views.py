from django.shortcuts import render, redirect
from core.models import Patient, Appointment, Billing, PrescriptionMedication

# Create your views here.

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("core:index")
    patientExists = Patient.objects.filter(user = request.user).exists()
    if patientExists is False:
        return redirect("core:index")
    patient = Patient.objects.get(user = request.user)
    appointments = patient.appointment_set.order_by('-appointment_date')[:3]
    billings = Billing.objects.filter(patient = patient.id)[:1]
    pms = PrescriptionMedication.objects.filter(prescription__patient = patient.id )
    latest_prescription = patient.prescription_set.order_by('-created_at').first()
    context = {"appointments": appointments, "billings": billings, "pms": pms, "latest_prescription": latest_prescription}
    return render(request, "dashboard.html", context)