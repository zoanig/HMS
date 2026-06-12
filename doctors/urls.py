from django.urls import path
from . import views

app_name = "doctors"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),

    path("appointments/history/", views.appointments, name="apt_history"),
    path("appointments/detail/<int:apt_id>/", views.get_appointment, name="apt_detail"),
    path("appointments/cancel/<int:apt_id>/", views.cancel_or_complete_appointment, name="apt_cancel"),
    path("appointments/complete/<int:apt_id>/", views.cancel_or_complete_appointment, name="apt_complete"),

    path("prescriptions/new/<int:patient_id>/", views.new_prescription, name="new_presc"),
    path("prescriptions/history/", views.prescriptionHistory, name="presc_history")
]

