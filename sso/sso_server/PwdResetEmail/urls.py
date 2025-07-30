from django.urls import path
from . import views

urlpatterns = [
    path('', views.reset_password_email, name='email_verification'),
]