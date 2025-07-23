# smul/academic/api_urls.py
from django.urls import path
from . import api_views

urlpatterns = [
    path('user-info/', api_views.get_user_info, name='get_user_info'),
    path('user-update/', api_views.update_user_info, name='update_user_info'),
    path('apply-leave/', api_views.apply_leave, name='apply_leave'),
]
