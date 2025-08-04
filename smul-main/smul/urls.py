from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('', include('smul.main.urls')),
    path('academic/', include('smul.academic.urls')),
    path('evaluation/', include('smul.evaluation.urls')),
    path('grade/', include('smul.grade.urls')),
    path('graduation/', include('smul.graduation.urls')),
    path('lecture/', include('smul.lecture.urls')),
    #path("handle-token/", lambda request: render(request, "main/handle_token.html")),

]
