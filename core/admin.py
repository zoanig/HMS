from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Patient)
admin.site.register(models.Doctor)
admin.site.register(models.Appointment)
admin.site.register(models.Medication)
admin.site.register(models.Prescription)
admin.site.register(models.PrescriptionMedication)
admin.site.register(models.Billing)
