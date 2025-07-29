from django.urls import path
from . import api_views

urlpatterns = [
    path('total/', api_views.total_grade_list_api, name='total_grade_list_api'),
]
