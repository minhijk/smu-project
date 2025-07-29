# smul/evaluation/api_urls.py
from django.urls import path
from .api_views import LectureSearchAPI, LectureEvalAPI

urlpatterns = [
    path('lecSearch', LectureSearchAPI.as_view(), name='api_lec_search'),
    path('lecEval', LectureEvalAPI.as_view(), name='api_lec_eval'),
]
