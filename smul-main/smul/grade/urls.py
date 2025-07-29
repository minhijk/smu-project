from django.urls import path
from . import views

urlpatterns = [
    path('all_grade_sch', views.all_grade_sch, name='all_grade_sch'),
]