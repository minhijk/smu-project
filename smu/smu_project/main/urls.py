from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('', views.home, name='home'),
    path('notice', views.notice_detail, name='notice_detail'),
    path('noticelist', views.notice_list, name='notice_list'),
    path('notice/search', views.notice_search, name='notice_search'),
    path('academic/calendar', views.academic_calendar, name='academic_calendar'),
    path('api/academic/calendar/',views.calendar_api,name='calendar_api'),
    path('logout/', views.logout, name='logout'),
    path('api/notice/filter', views.notice_filter_api, name='notice_filter_api'),
    path('search/', views.notice_search, name='notice_search'),

    path('api/notice/update/', views.update_notice, name='update_notice'),
    path('api/notice/create/', views.create_notice, name='create_notice'),
    path('api/notice/delete/', views.delete_notice, name='delete_notice'),
    path('notice/create/', views.notice_create_page, name='notice_create_page'),

    path('api/academic/calendar/create/', views.create_event),
    path('api/academic/calendar/update/<int:pk>/', views.update_event),
    path('api/academic/calendar/delete/<int:pk>/', views.delete_event),

    path("handle-token/", lambda request: render(request, "main/handle_token.html")),
]