from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Doctor, Appointment, PrescriptionMedication, Patient, Prescription
from django.db.models import Sum
from django.urls import reverse
from .forms import PrescriptionForm, PrescriptionMedicationFormSet
import humanize

# Create your views here.

@login_required
def dashboard(request):
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        return redirect("core:index")
    latest_appointments = Appointment.objects.filter(doctor = doctor, status = Appointment.Status.SCHEDULED).order_by("-appointment_date")[:3]
    total_completed_appointments = Appointment.objects.filter(doctor = doctor, status = Appointment.Status.COMPLETED).count()
    total_scheduled_appointments = Appointment.objects.filter(doctor = doctor, status = Appointment.Status.SCHEDULED).count()
    revenue_with_medications = PrescriptionMedication.objects.filter(prescription__doctor = doctor).aggregate(total=Sum('medication__price'))['total']

    total_medication_prescribed = PrescriptionMedication.objects.filter(prescription__doctor = doctor).count()
    context = {
        "latest_appointments": latest_appointments, 
        "total_completed_appointments": total_completed_appointments, 
        "total_medication_prescribed": total_medication_prescribed,
        "total_scheduled_appointments": total_scheduled_appointments,
        "revenue_with_medications": revenue_with_medications
        }
    return render(request, "d_dashboard.html", context)

@login_required
def appointments(request):
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        return redirect("core:index")
    apts = Appointment.objects.filter(doctor = doctor).order_by("-appointment_date")
    context = {"apts": apts}
    return render(request, "d_apt_history.html", context)

@login_required
def get_appointment(request, apt_id):
    try:
        doctor = request.user.doctor
        apt = Appointment.objects.get(id=apt_id, doctor=doctor)
    except Doctor.DoesNotExist:
        return redirect("core:index")
    except Appointment.DoesNotExist:
        return render(request, "core/404.html", {"message": "The resource you are trying to access doesnt. Or you're unauthorized to access it"})
    time = f"{apt.status} {humanize.naturaltime(apt.appointment_date)}"
    context = {"apt": apt, "time": time}
    return render(request, "d_appointment_detail.html", context)

@login_required
def cancel_or_complete_appointment(request, apt_id):
    try:
        doctor = request.user.doctor
        apt = Appointment.objects.get(id=apt_id, doctor=doctor)
    except Doctor.DoesNotExist:
        return redirect("core:index")
    except Appointment.DoesNotExist:
        return render(request, "core/404.html", {"message": "The resource you are trying to access doesnt. Or you're unauthorized to access it"})
    if apt.status == Appointment.Status.SCHEDULED:
        if request.path == reverse("doctors:apt_cancel", args=[apt_id]):
            apt.status = Appointment.Status.CANCELLED
        elif request.path == reverse("doctors:apt_complete", args=[apt_id]):
            apt.status = Appointment.Status.COMPLETED
        apt.save()
    return redirect("doctors:apt_detail", apt_id=apt_id)


@login_required
def prescriptionHistory(request):
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        return redirect("core:index")
    prescs = Prescription.objects.filter(doctor=doctor).order_by("-created_at")
    context = {"prescs": prescs}
    return render(request, "d_prescription_history.html", context)

@login_required
def new_prescription(request, patient_id):
    try:
        doctor = request.user.doctor
        patient = Patient.objects.get(id=patient_id)
    except Doctor.DoesNotExist:
        return redirect("core:index")
    except Patient.DoesNotExist:
        return redirect("core:index")

    if request.method == "POST":

        prescription_form = PrescriptionForm(request.POST)
        temp_prescription = Prescription(patient=patient, doctor=doctor)
        medication_formset = PrescriptionMedicationFormSet(request.POST,instance=temp_prescription)

        if prescription_form.is_valid() and medication_formset.is_valid():

            prescription = prescription_form.save(commit=False)

            prescription.patient = patient
            prescription.doctor = doctor

            prescription.save()

            medication_formset.instance = prescription

            medication_formset.save()

            return redirect("doctors:dashboard")

    else:

        prescription_form = PrescriptionForm()

        medication_formset = PrescriptionMedicationFormSet()

    return render(
        request,
        "d_new_prescription.html",
        {
            "patient": patient,
            "form": prescription_form,
            "formset": medication_formset
        }
    )