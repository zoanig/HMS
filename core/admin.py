from django.contrib import admin
from . import models
# Register your models here.

class IntermediaryInline(admin.TabularInline):
    model = models.PrescriptionMedication
    extra = 1

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'meds', 'created_at']
    list_filter = ['doctor', 'patient', 'created_at']

    inlines = [IntermediaryInline]

    fieldsets = [
        ("Relation Info", {
            "fields" : ["patient", "doctor"]
        }),
    ]

    def meds(self, obj):
        smeds = []
        meds = obj.medications.all()
        for med in meds[:2]:
            smeds.append(med.name)

        return ",".join(smeds) + "..."

class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date' ,'status']
    search_fields = ['patient__name', 'doctor__name']

admin.site.register(models.Patient)
admin.site.register(models.Doctor)
admin.site.register(models.Appointment, AppointmentsAdmin)
admin.site.register(models.Medication)
admin.site.register(models.Prescription, PrescriptionAdmin)
admin.site.register(models.PrescriptionMedication)
admin.site.register(models.Billing)
