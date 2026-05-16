from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        CUSTOM = 'C', 'Custom'
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.CUSTOM)
    contact_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    availability_schedule = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'Scheduled'
        CANCELLED = 'Cancelled'
        COMPLETED = 'Completed'
    patient = models.ForeignKey(Patient ,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor ,on_delete=models.CASCADE)
    appointment_date = models.DateField()
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.SCHEDULED)

    def __str__(self):
        return f"Appointment ID #{self.id}"

class Medication(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    patient = models.ForeignKey(Patient ,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor ,on_delete=models.CASCADE)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    medications = models.ManyToManyField(
    Medication,
    through='PrescriptionMedication'
)

    def __str__(self):
        return f"Prescription ID #{self.id}"


class PrescriptionMedication(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    duration = models.DurationField()

class Billing(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending'
        PAID = 'Paid'
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=7, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.patient.name} - {self.payment_status}"
    


