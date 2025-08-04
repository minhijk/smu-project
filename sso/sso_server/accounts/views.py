from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


class LogoutView(APIView):
    """
    사용자가 로그아웃할 때 refresh token을 서버 측 블랙리스트에 등록합니다.
    이로써 더 이상 이 refresh token으로 access token을 재발급받을 수 없게 됩니다.
    """
    permission_classes = [IsAuthenticated]  # access token이 유효해야 로그아웃 허용

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh", None)

            if refresh_token is None:
                return Response({"error": "refresh token이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # 블랙리스트에 등록
            return Response({"detail": "로그아웃 되었습니다."}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"error": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        print("✅ POST 요청 도달함")
        return super().post(request, *args, **kwargs)

from django.conf import settings
from accounts.models import EmailAuthCode
from accounts.models import CustomUser
from solapi import SolapiMessageService
from solapi.model import RequestMessage
import random, string
from django.core.mail import send_mail

# 테스트용: 학번+이름 → 전화번호 매핑

FAKE_USER_DB = {
    ('202321290', '강민서'): '01095218200',
    ('20240001', '김교수'): '01098765432',
    ('202121320', '이민혁'): '01098297141'
}

def generate_temp_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


# ✅ SMS 전송 함수 (SOLAPI)
def send_sms(to, text):
    service = SolapiMessageService(
        api_key=settings.SOLAPI_API_KEY,
        api_secret=settings.SOLAPI_API_SECRET
    )
    message = RequestMessage(from_=settings.SOLAPI_SENDER, to=to, text=text)
    try:
        response = service.send(message)
        print("📨 전송 성공:", response)
        return True
    except Exception as e:
        print("❌ 전송 실패:", e)
        return False


@api_view(['POST'])
@permission_classes([AllowAny])
def send_code(request):
    student_id = request.data.get("student_id")
    name = request.data.get("name")

    phone = FAKE_USER_DB.get((student_id, name))
    if not phone:
        return Response({"error": "사용자 정보 없음"}, status=404)

    code = str(random.randint(100000, 999999))
    EmailAuthCode.objects.create(student_id=student_id, name=name, phone=phone, code=code)

    text = f"[샘물] 인증번호는 {code}입니다. 3분 내 입력하세요."
    send_sms(phone, text)

    return Response({"success": True})


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_code(request):
    student_id = request.data.get("student_id")
    code_input = request.data.get("code")

    latest = EmailAuthCode.objects.filter(student_id=student_id).order_by('-created_at').first()
    if not latest or latest.code != code_input or latest.is_expired():
        return Response({"error": "인증번호 오류 또는 만료"}, status=400)

    try:
        user = CustomUser.objects.get(student_id=student_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "해당 계정 없음"}, status=404)

    temp_password = generate_temp_password()
    user.set_password(temp_password)
    user.save()

    return Response({"success": True, "temp_password": temp_password})

# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from accounts.models import EmailAuthCode, CustomUser
import random, string

# 임시 비밀번호 생성
def generate_temp_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

# 이메일 DB (임시)
FAKE_USER_DB = {
    ('202321290', '강민서'): 'snrntpsy0629@naver.com',
    ('20240001', '김교수'): 'kim@smu.ac.kr',
    ('202121320', '이민혁'): 'hyeok7141@daum.net'
}

@api_view(['POST'])
@permission_classes([AllowAny])
def send_email_code(request):
    student_id = request.data.get("student_id")
    name = request.data.get("name")

    email = FAKE_USER_DB.get((student_id, name))
    if not email:
        return Response({"error": "사용자 정보 없음"}, status=404)

    code = str(random.randint(100000, 999999))
    EmailAuthCode.objects.create(student_id=student_id, name=name, email=email, code=code)

    try:
        send_mail(
            '샘물 비밀번호 초기화 인증번호',
            f'인증번호는 {code} 입니다. 3분 내 입력해 주세요.',
            'noreply@smu.ac.kr',
            [email],
            fail_silently=False
        )
        return Response({"success": True})
    except:
        return Response({"error": "이메일 전송 실패"}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email_code(request):
    student_id = request.data.get("student_id")
    code_input = request.data.get("code")

    latest = EmailAuthCode.objects.filter(student_id=student_id).order_by('-created_at').first()
    if not latest or latest.code != code_input or latest.is_expired():
        return Response({"error": "인증번호 오류 또는 만료"}, status=400)

    try:
        user = CustomUser.objects.get(student_id=student_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "계정 없음"}, status=404)

    temp_pw = generate_temp_password()
    user.set_password(temp_pw)
    user.save()

    return Response({"success": True, "temp_password": temp_pw})

