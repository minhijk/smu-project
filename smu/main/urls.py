from django.urls import path
from . import views
from main.views import logout

urlpatterns = [
    path('', views.home, name='home'),
    path('notice', views.notice_detail, name='notice_detail'),
    path('noticelist', views.notice_list, name='notice_list'),
    path('notice/search', views.notice_search, name='notice_search'),
    path('academic/calendar', views.academic_calendar, name='academic_calendar'),
    path('api/academic/calendar',views.calendar_api,name='calendar_api'),
    path('login',views.login,name='login'),
    path('logout/', logout, name='logout'),
]