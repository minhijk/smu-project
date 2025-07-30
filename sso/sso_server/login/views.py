from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as django_logout
from django.contrib import messages
from django.http import HttpResponse

def password_reset(request):
    return render(request, 'login/password_reset.html')
