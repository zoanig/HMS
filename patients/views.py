from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from core.models import Patient, Appointment, Billing, PrescriptionMedication, Doctor
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import PatientProfile, AppointmentForm
from .utils import get_patinet_or_redirect, generate_slots
import humanize
from datetime import datetime, time


# Create your views here.
@login_required
def dashboard(request):
    patient = get_patinet_or_redirect(request, "core:index")
    if not isinstance(patient, Patient):
        return patient
    appointments = patient.appointment_set.order_by('-appointment_date')
    total_appointments = appointments.count()
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
    try:
        apt = patient.appointment_set.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, "core/404.html", {"message": "The resource you are trying to access doesnt. Or you're unauthorized to access it"})
    time = f"{apt.status} {humanize.naturaltime(apt.appointment_date)}"
    context = {"apt": apt, "time": time}
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
    
@login_required
def prescription_detail(request, pk):
    patient = get_patinet_or_redirect(request, "core:index")
    if not isinstance(patient, Patient):
        return patient
    try:
        presc = patient.prescription_set.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, "core/404.html", {"message": "The resource you are trying to access doesnt exist. Or you're unauthorized to access it"})
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

@login_required
def get_profile(request):
    patient = get_patinet_or_redirect(request, "core:index")
    if not isinstance(patient, Patient):
        return patient
    context = {"patient": patient}
    return render(request, "patient_profile.html", context)

@login_required
def edit_profile(request):
    patient = get_patinet_or_redirect(request, "core:index")
    if not isinstance(patient, Patient):
        return patient
    if request.method == 'POST':
        form = PatientProfile(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("patients:profile")
    
    form = PatientProfile(instance=patient)
    context = {"form": form}
    return render(request, "patient_profile_edit.html", context)

@login_required
def cancel_appointment(request, pk):
    patient = get_patinet_or_redirect(request, "core:index")
    if not isinstance(patient, Patient):
        return patient
    try:
        apt = patient.appointment_set.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, "core/404.html", {"message": "The resource you are trying to access doesnt exist. Or you're unauthorized to access it"})
    if apt.status == Appointment.Status.SCHEDULED:
        apt.status = Appointment.Status.CANCELLED
        apt.save()
    return redirect("patients:appointment", pk=pk)


@login_required
def new_profile(request):
    patient = get_patinet_or_redirect(request, "core:index")
    is_doctor = Doctor.objects.filter(user=request.user).exists()
    if isinstance(patient, Patient) or is_doctor:
        return redirect("core:index")
    if request.method == 'POST':
        form = PatientProfile(request.POST)
        if form.is_valid():
            patient = Patient.objects.create(**form.cleaned_data, user=request.user)
            patient.save()
            return redirect("patients:dashboard")
    else:
        form = PatientProfile()
    context = {"form": form}
    return render(request, "new_patient_profile.html", context)


@login_required
def available_slots(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)

    date_string = request.GET.get("date")

    if not date_string:
        return JsonResponse({"slots": []})

    selected_date = datetime.strptime(
        date_string,
        "%Y-%m-%d"
    ).date()

    all_slots = generate_slots(selected_date)
    start_of_day = timezone.make_aware(
        datetime.combine(selected_date, time.min)
    )

    end_of_day = timezone.make_aware(
        datetime.combine(selected_date, time.max)
    )
    booked = Appointment.objects.filter(
    doctor=doctor,
    status=Appointment.Status.SCHEDULED,
    appointment_date__range=(start_of_day, end_of_day)
    )

    start = timezone.make_aware(datetime.combine(selected_date, time.min))
    end = timezone.make_aware(datetime.combine(selected_date, time.max))

    booked_times = set(
        Appointment.objects.filter(
            doctor=doctor,
            status=Appointment.Status.SCHEDULED,
            appointment_date__range=(start, end)
        ).values_list("appointment_date__time", flat=True)
    )

    available = [
        slot.strftime("%H:%M")
        for slot in all_slots
        if slot.strftime("%H:%M") not in {
            t.strftime("%H:%M") for t in booked_times
        }
    ]

    return JsonResponse({
        "slots": available
    })

@login_required
def new_appointment(request, doctor_id):
    doctor = get_object_or_404(
        Doctor,
        pk=doctor_id
    )

    patient = get_object_or_404(
        Patient,
        user=request.user
    )

    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    appointment = Appointment(
                        patient=patient,
                        doctor=doctor,
                        appointment_date=form.cleaned_data[
                            "appointment_datetime"
                        ]
                    )

                    appointment.full_clean()
                    appointment.save()

                messages.success(
                    request,
                    "Appointment booked successfully."
                )

                return redirect("patients:dashboard")

            except ValidationError as e:
                form.add_error(
                    None,
                    e.message_dict if hasattr(e, "message_dict")
                    else e.messages
                )

    else:
        form = AppointmentForm()

    return render(
        request,
        "new_appointment.html",
        {
            "form": form,
            "doctor": doctor,
        }
    )

@login_required
def doctor_list(request):
    patient = get_patinet_or_redirect(request, "core:index")
    if not isinstance(patient, Patient):
        return patient
    
    doctors = Doctor.objects.all()
    return render(request, "doctor_list.html", {"doctors": doctors})