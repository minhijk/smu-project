from django.urls import path
from . import api_views

urlpatterns = [
    path('gradCreditCheck', api_views.grad_credit_check, name='grad_credit_check'),
]
