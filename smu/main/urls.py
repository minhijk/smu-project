from django.urls import path
from . import views
from login import views as login_views
urlpatterns = [
    path('', views.home, name='home'),
    path('notice', views.notice_detail, name='notice_detail'),
    path('noticelist', views.notice_list, name='notice_list'),
    path('notice/search', views.notice_search, name='notice_search'),
    path('academic/calendar', views.academic_calendar, name='academic_calendar'),
    path('api/academic/calendar/',views.calendar_api,name='calendar_api'),
    # 로그아웃 경로 추가
    path('logout/', login_views.logout, name='logout'),
        path('api/notice/filter', views.notice_filter_api, name='notice_filter_api'),
    path('search/', views.notice_search, name='notice_search'),
]
