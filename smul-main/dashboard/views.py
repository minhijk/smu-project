from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    # 더미 공지사항 (→ 추후 외부 API로 대체 예정)
    notice_data = [
        {"title": "[학사] 여름 계절학기 수강신청 안내"},
        {"title": "[일반] 스마트학생증 신청 방법"},
        {"title": "[장학] 국가장학금 2차 신청 안내"},
        {"title": "[취업] 인턴십 설명회 개최 안내"},
        {"title": "[교내] 기말고사 대비 학습법 특강"},
    ]

    # 더미 학점 현황 (→ 추후 DB 또는 사용자별 API 연동 예정)
    grade_info = {
        "total": 96,
        "required": 130,
        "major": 54,
        "liberal": 42
    }

    # 더미 시간표 (→ 추후 다른 팀원 시스템에서 사용자별 연동 예정)
    timetable_data = [
        {"day": "월", "subject": "웹프로그래밍", "time": "09:00~10:30"},
        {"day": "화", "subject": "보안개론", "time": "10:30~12:00"},
        {"day": "수", "subject": "IoT 실습", "time": "13:00~14:30"},
    ]

    context = {
        "notice_list": notice_data,
        "grade": grade_info,
        "timetable": timetable_data,
        "username": request.user.username,
    }
    return render(request, 'home.html', context)
