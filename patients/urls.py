from django.urls import path
from . import views
app_name = "patients"

urlpatterns = [
    path("dashboard/", views.dashboard, name='dashboard'),
    path("appointment/<int:pk>", views.get_appointment, name='appointment'),
    path("appointments/history/", views.appointments_history, name="apt_history"),
    path("prescriptions/history/", views.prescription_history, name="pres_history"),
    path("prescription/<int:pk>", views.prescription_detail, name='presc'),
    path("medications/history/", views.medication_history, name="meds")
]
