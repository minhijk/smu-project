from django.urls import path
from . import views

urlpatterns = [
    path('enrollment/', views.enrollment_page, name='enrollment_page'),
]
