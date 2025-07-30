# PwdResetSMS/views.py
from django.shortcuts import render

def reset_password_sms(request):
    return render(request, "PwdResetSMS/SMS_reset.html")
