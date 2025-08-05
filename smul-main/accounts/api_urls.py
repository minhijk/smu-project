from django.urls import path
from . import api_views

urlpatterns = [
    path('user', api_views.get_user_info, name='api_user'),
    path('user_update', api_views.update_user_info, name='api_user_update'),
    path('password/', api_views.change_user_password, name='change_password'),
    path('profile/', api_views.update_user_address, name='profile'),
    path('message/', api_views.message_box, name='message_box'),  # 쪽지함
    path('todo/', api_views.todo_page, name='todo'),    
    path('api/user/',api_views.UserInfoAPIView.as_view(), name='api_user'),

    path("api/update-profile/", api_views.update_profile_api, name="update_profile_api"),
]
