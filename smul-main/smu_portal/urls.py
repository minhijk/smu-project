from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/api/', include('accounts.api_urls')),  # ✅ 추가!
    path('smul/', include('smul.urls')),
]
