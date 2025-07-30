# PwdResetSMS/views.py
from django.shortcuts import render

def reset_password_email(request):
    return render(request, "PwdResetEmail/email_reset.html")
