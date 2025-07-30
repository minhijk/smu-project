from django.urls import path
from . import views

urlpatterns = [
    path("", views.reset_password_sms, name="SMS_reset"),
]
