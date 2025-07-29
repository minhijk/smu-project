from django.urls import path
from . import views

urlpatterns = [
    # ✅ 로그인/로그아웃
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ✅ 사용자 정보 페이지 (템플릿 렌더링용)
    path('profile/', views.user_info_page, name='profile'),  # 개인정보 탭
    path('password/', views.change_password, name='change_password'),  # 비밀번호 변경 탭
    path('message/', views.message_box, name='message_box'),  # 쪽지함
    path('todo/', views.todo_page, name='todo'),              # 일정관리

    # ✅ 주소 정보 POST 처리
    path('update_address/', views.update_user_address, name='update_user_address'),

    # ✅ REST API
    path('api/user/', views.UserInfoAPIView.as_view(), name='api_user'),
    path('api/user_update/', views.UserUpdateAPIView.as_view(), name='api_user_update'),
    path('api/change_password/', views.ChangePasswordAPIView.as_view(), name='api_change_password'),

    # ✅ 기타 사용자 정보 조회용 URL
    path('user_info/', views.user_info_page, name='user_info_page'),  # 중복되더라도 유지 가능 (profile과 같은 뷰)
]
