from django.urls import path
from . import api_views

urlpatterns = [
    path('user', api_views.get_user_info, name='api_user'),
    path('user_update', api_views.update_user_info, name='api_user_update'),
]
