from django.shortcuts import render, redirect
from core.models import Patient, Appointment

# Create your views here.

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("core:index")
    patient = Patient.objects.get(user = request.user)
    if patient is None:
        return redirect("core:index")
    appointments = Appointment.objects.filter(patient = patient.id)
    context = {"appointments": appointments}
    return render(request, "dashboard.html", context)