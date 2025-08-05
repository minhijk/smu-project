from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import handle_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.api_urls')),
    path('smul/', include('smul.urls')),
    path('academic/', include('smul.academic.urls')),
    path('api/academic/',include('smul.academic.api_urls')),
    path('lecture/', include('smul.lecture.urls')),
    path('api/lecture/', include('smul.lecture.api_urls')),
    path('grade/', include('smul.grade.urls')),
    path('api/grade/', include('smul.grade.api_urls')),
    path('evaluation/', include('smul.evaluation.urls')),            
    path('api/evaluation/', include('smul.evaluation.api_urls')),    
    path('graduation/', include('smul.graduation.urls')),            
    path('api/graduation/', include('smul.graduation.api_urls')),
    path("handle-token/", handle_token),
]

# 개발 환경에서 media 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
