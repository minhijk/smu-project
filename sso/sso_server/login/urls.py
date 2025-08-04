from django.urls import path
from . import  views
from django.views.generic import TemplateView


app_name = 'login'

urlpatterns = [
    path('', TemplateView.as_view(template_name="login/login.html"), name='login'),
    path('reset/', views.password_reset, name='password_reset'),
]
