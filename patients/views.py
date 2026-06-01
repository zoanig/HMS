from django.shortcuts import render, redirect
from core.models import Patient, Appointment, Billing, PrescriptionMedication
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("core:index")
    patientExists = Patient.objects.filter(user = request.user).exists()
    if patientExists is False:
        return redirect("core:index")
    patient = Patient.objects.get(user = request.user)
    appointments = patient.appointment_set.order_by('-appointment_date')
    total_appointments = len(appointments)
    billings = Billing.objects.filter(patient = patient.id)[:1]
    pms = PrescriptionMedication.objects.filter(prescription__patient = patient.id )
    latest_prescription = patient.prescription_set.order_by('-created_at').first()
    context = {"appointments": appointments[:2], "billings": billings, "pms": pms, "latest_prescription": latest_prescription, "total_appointments": total_appointments}
    return render(request, "dashboard.html", context)

def get_appointment(request, pk):
    if not request.user.is_authenticated:
        return redirect("core:index")
    patientExists = Patient.objects.filter(user = request.user).exists()
    if patientExists is False:
        return redirect("core:index")
    patient = Patient.objects.get(user = request.user)
    apt = ""
    try:
        apt = patient.appointment_set.get(id=pk)
        print(apt)
    except ObjectDoesNotExist:
        return render(request, "core/404.html", {"message": "The resource you are trying to access doesnt. Or you're unauthorized to access it"})
    
    context = {"appointment": apt}
    return 
