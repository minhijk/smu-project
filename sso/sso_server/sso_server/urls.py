from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from accounts.views import send_code, verify_code, send_email_code
from accounts.views import send_email_code, verify_email_code
from accounts.views import LogoutView, CustomTokenObtainPairView  # ✅ 이 줄이 꼭 필요합니다!
from django.urls import path

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/logout/', LogoutView.as_view(), name="token_logout"),
    path('api/send-code/', send_code, name='send_code'),
    path('api/verify-code/', verify_code, name= 'verify_code'),
    path('api/send-email-code/', send_email_code, name='send_email_code'),
    path('api/verify-email-code/', verify_email_code, name='verify_email_code'),

    path('login/', include('login.urls')),
    path('PwdResetEmail/', include('PwdResetEmail.urls')),
    path('PwdResetSMS/', include('PwdResetSMS.urls')),
]


