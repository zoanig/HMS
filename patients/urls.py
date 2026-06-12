from django.urls import path
from . import views
app_name = "patients"

urlpatterns = [
    path("dashboard/", views.dashboard, name='dashboard'),

    path("appointment/<int:pk>/", views.get_appointment, name='appointment'),
    path("appointment/cancel/<int:pk>", views.cancel_appointment, name="apt_cancel"),
    path("appointments/history/", views.appointments_history, name="apt_history"),
    path("appointment/new/<int:doctor_id>", views.new_appointment, name="apt_new"),

    path("availableslots/<int:doctor_id>", views.available_slots, name='available_slots' ),

    path("prescriptions/history/", views.prescription_history, name="pres_history"),
    path("prescription/<int:pk>/", views.prescription_detail, name='presc'),

    path("medications/history/", views.medication_history, name="meds"),

    path("profile/", views.get_profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/new/", views.new_profile, name="new_profile"),

    path("doctorlist/", views.doctor_list, name="d_list")

]
