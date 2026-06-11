from django import forms
from core.models import Patient, Appointment
from django.utils import timezone

class PatientProfile(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'gender', 'contact_number', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

class AppointmentForm(forms.Form):
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    appointment_time = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"})
    )

    def clean(self):
        cleaned_data = super().clean()

        date = cleaned_data.get("appointment_date")
        time = cleaned_data.get("appointment_time")

        if not date or not time:
            return cleaned_data

        appointment_datetime = timezone.make_aware(
            timezone.datetime.combine(date, time)
        )

        if appointment_datetime <= timezone.now():
            raise forms.ValidationError(
                "You cannot schedule an appointment in the past."
            )

        cleaned_data["appointment_datetime"] = appointment_datetime

        return cleaned_data