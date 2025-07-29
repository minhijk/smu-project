# dashboard/views.py
import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from smul.academic.models import StudentProfile

@login_required
def home(request):
    # 1. 공지사항 (더미 데이터)
    notice_data = [
        {"title": "[학사] 여름 계절학기 수강신청 안내"},
        {"title": "[일반] 스마트학생증 신청 방법"},
        {"title": "[장학] 국가장학금 2차 신청 안내"},
        {"title": "[취업] 인턴십 설명회 개최 안내"},
        {"title": "[교내] 기말고사 대비 학습법 특강"},
    ]

    # 2. 학점 현황 (DB 연동)
    try:
        profile = StudentProfile.objects.get(user=request.user)
        grade_info = {
            "total": profile.total_credit,
            "major": profile.major_credit,
            "liberal": profile.liberal_credit,
            "general": profile.general_credit,
            "teaching": profile.teaching_credit,
            "etc": profile.etc_credit,
            "gpa": profile.gpa
        }
    except StudentProfile.DoesNotExist:
        grade_info = {
            "total": 0,
            "major": 0,
            "liberal": 0,
            "general": 0,
            "teaching": 0,
            "etc": 0,
            "gpa": 0.0
        }

    # 3. 시간표 (더미 데이터)
    timetable_data = [
        {"day": "월", "subject": "웹프로그래밍", "time": "09:00~10:30"},
        {"day": "화", "subject": "보안개론", "time": "10:30~12:00"},
        {"day": "수", "subject": "IoT 실습", "time": "13:00~14:30"},
    ]

    # 4. 날씨 정보
    api_key = "7e99b0af1e28436ea75182843252507"
    weather = {}

    try:
        res = requests.get(
            f"https://api.weatherapi.com/v1/current.json?key={api_key}&q=Cheonan&lang=ko", timeout=3
        )
        data = res.json()
        weather = {
            "temp": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"],
            "humidity": data["current"]["humidity"]
        }
    except Exception:
        weather = {
            "temp": "정보 없음",
            "condition": "날씨 정보를 불러올 수 없습니다.",
            "icon": "",
            "humidity": "-"
        }

    context = {
        "notice_list": notice_data,
        "grade": grade_info,
        "timetable": timetable_data,
        "username": request.user.username,
        "weather": weather
    }

    return render(request, 'home.html', context)
