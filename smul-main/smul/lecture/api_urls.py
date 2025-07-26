from django.urls import path
from . import api_views

urlpatterns = [
    path('enrolled/', api_views.enrolled_lectures_api, name='enrolled_lectures_api'),
]
