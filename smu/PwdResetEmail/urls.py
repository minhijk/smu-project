from django.urls import path
from . import views

urlpatterns = [
    path('', views.email_verification_view, name='email_verification'),
]