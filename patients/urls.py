from django.urls import path
from . import views
app_name = "patients"

urlpatterns = [
    path("dashboard/", views.dashboard, name='dashboard'),
    path("appointment/<int:pk>", views.get_appointment, name='appointment')
]
