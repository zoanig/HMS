from django import forms
from core.models import Prescription, PrescriptionMedication

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["notes"]

        widgets = {
            "notes": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 4
                }
            )
        }

class PrescriptionMedicationForm(forms.ModelForm):

    class Meta:
        model = PrescriptionMedication

        fields = [
            "medication",
            "dosage",
            "duration"
        ]

        widgets = {
            "medication": forms.Select(
                attrs={
                    "class": "select select-bordered w-full"
                }
            ),

            "dosage": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full"
                }
            ),

            "duration": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Days"
                }
            )
        }

PrescriptionMedicationFormSet = forms.inlineformset_factory(
    Prescription,
    PrescriptionMedication,
    form=PrescriptionMedicationForm,
    extra=1,
    can_delete=True
)