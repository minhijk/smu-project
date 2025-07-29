from django.urls import path
from . import views


urlpatterns = [
    path('grad_credit_sch/', views.grad_credit_sch, name='grad_credit_sch'),
]
