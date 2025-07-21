from django.urls import path, include

urlpatterns = [
    path('', include('smul.main.urls')),
    path('academic/', include('smul.academic.urls')),
    path('evaluation/', include('smul.evaluation.urls')),
    path('grade/', include('smul.grade.urls')),
    path('graduation/', include('smul.graduation.urls')),
    #path('lecture/', include('smul.lecture.urls')),
    #path('registration/', include('smul.registration.urls')),
]
