from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
from PwdResetEmail.models import EmailAuthCode
from django.conf import settings
import random, requests
from solapi import SolapiMessageService  # ✔️ official SDK
from solapi.model import RequestMessage

# 테스트용: 학번+이름 → 전화번호 매핑 (실제 서비스 시 DB로 교체)
FAKE_USER_DB = {
    ('202321290', '강민서'): '01036596467',
    ('20240001', '김교수'): '01098765432',
}

import jwt
import uuid
import time
import requests

def send_sms(to, text):
    service = SolapiMessageService(
        api_key=settings.SOLAPI_API_KEY,
        api_secret=settings.SOLAPI_API_SECRET
    )
    message = RequestMessage(
        from_=settings.SOLAPI_SENDER,
        to=to,
        text=text
    )
    try:
        response = service.send(message)
        print("📨 전송 성공:", response)
        return True
    except Exception as e:
        print("❌ 전송 실패:", e)
        return False

def reset_password_sms(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        code_input = request.POST.get('code')
        action = request.POST.get('action')

        phone = FAKE_USER_DB.get((student_id, name))
        if not phone:
            messages.error(request, '사용자 정보를 찾을 수 없습니다.')
            return render(...)

        if action == 'send':
            recent = EmailAuthCode.objects.filter(student_id=student_id, name=name).order_by('-created_at').first()
            if recent and recent.is_re_request_blocked():
                messages.error(request, '1분 후에 다시 요청해주세요.')
            else:
                code = str(random.randint(100000, 999999))
                EmailAuthCode.objects.create(student_id=student_id, name=name, email='', code=code)
                text = f"[샘물] 인증번호는 {code}입니다. 3분 내 입력하세요."
                if send_sms(phone, text):
                    messages.success(request, f"{phone[-4:]}번으로 인증번호를 보냈습니다.")
                else:
                    messages.error(request, "SMS 전송에 실패했습니다.")
            return render(...)
        
    api_key = settings.SOLAPI_API_KEY
    api_secret = settings.SOLAPI_API_SECRET
    sender = settings.SOLAPI_SENDER

    payload = {
        'access_key': api_key,
        'nonce': str(uuid.uuid4()),
        'timestamp': int(time.time() * 1000)
    }
    token = jwt.encode(payload, api_secret, algorithm='HS256')

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # ✅ messages 배열로 수정
    message_obj = {
        "to": to,
        "from": sender,
        "text": text,
        "type": "LMS",
        "clientId": str(uuid.uuid4())  
    }

    body = {
        "messages": [message_obj]  # ✅ 배열로 감싸야 함
    }

    print("📦 최종 전송 body:", body)

    response = requests.post("https://api.solapi.com/messages/v4/send", headers=headers, json=body)

    print("📨 응답 코드:", response.status_code)
    print("📨 응답 본문:", response.text)

    return response.status_code == 200

    


def reset_password_sms(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        code_input = request.POST.get('code')
        action = request.POST.get('action')

        phone = FAKE_USER_DB.get((student_id, name))
        if not phone:
            messages.error(request, '사용자 정보를 찾을 수 없습니다.')
            return render(request, "PwdResetSMS/SMS_reset.html")

        if action == 'send':
            recent = EmailAuthCode.objects.filter(student_id=student_id, name=name).order_by('-created_at').first()
            if recent and recent.is_re_request_blocked():
                messages.error(request, '1분 후에 다시 요청해주세요.')
            else:
                code = str(random.randint(100000, 999999))
                EmailAuthCode.objects.create(student_id=student_id, name=name, email='', phone = phone, code=code)
                success = send_sms(phone, f"[샘물] 인증번호는 {code}입니다. 3분 내 입력하세요.")
                if success:
                    messages.success(request, f"{phone[-4:]}번으로 인증번호를 보냈습니다.")
                else:
                    messages.error(request, "SMS 전송에 실패했습니다.")
            return render(request, "PwdResetSMS/SMS_reset.html")

        elif action == 'confirm':
            latest = EmailAuthCode.objects.filter(student_id=student_id, name=name).order_by('-created_at').first()
            if latest and latest.code == code_input and not latest.is_expired():
                latest.is_verified = True
                latest.save()
                messages.success(request, "✅ SMS 인증이 완료되었습니다.")
                return render(request, "PwdResetSMS/SMS_success.html")
            else:
                messages.error(request, "인증번호가 올바르지 않거나 만료되었습니다.")
                return render(request, "PwdResetSMS/SMS_reset.html")

    return render(request, "PwdResetSMS/SMS_reset.html")
