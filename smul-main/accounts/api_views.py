from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from dashboard.utils import decode_jwt_from_request
from django.shortcuts import redirect, render
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

import json
from django.http import JsonResponse

# --------------------------
# ✅ 여기만 jwt 인증 사용 - 샘물 -> 상명대로 이동할 때 필요함
# --------------------------
class UserInfoAPIView(APIView):
    def get(self, request):
        # ✅ 우선 Django 로그인 사용자 우선 처리
        if request.user.is_authenticated:
            return Response({
                'username': request.user.username,
                'first_name': request.user.first_name
            })

        # 그게 안 되면 세션에 저장된 access_token 기반으로 판단
        payload = decode_jwt_from_request(request)
        if not payload:
            return Response({'error': 'unauthorized'}, status=401)

        return Response({
            'username': payload.get("student_id"),
            'first_name': payload.get("name")
        })
    
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("/")

@api_view(['GET'])
@permission_classes([AllowAny])  # 🔄 모든 요청 허용 후 내부에서 판단
def get_user_info(request):
    if request.user.is_authenticated:
        return Response({
            'id': request.user.username,
            'name': request.user.first_name
        })

    # JWT로 로그인 여부 확인
    payload = decode_jwt_from_request(request)
    if not payload:
        return Response({'error': 'unauthorized'}, status=401)

    return Response({
        'id': payload.get("student_id"),
        'name': payload.get("name")
    })


# ✅ SMUL 측에서 SSO API 호출을 위한 함수 (세션에서 JWT 꺼내기)

import requests
from django.conf import settings

def get_jwt_from_session(request):
    return request.session.get('access_token')

# ✅ SSO API Base URL
SSO_API_BASE = 'http://localhost:8001/api'  # 실제 주소에 맞게 변경

# ----------------------
# 1. GET 사용자 정보
# ----------------------
def fetch_user_info(request):
    token = get_jwt_from_session(request)
    if not token:
        return None, 'JWT 토큰이 없습니다.'

    headers = {
        'Authorization': f'Bearer {token}'
    }
    try:
        res = requests.get(f'{SSO_API_BASE}/user-info/', headers=headers)
        if res.status_code == 200:
            return res.json(), None
        return None, res.json().get('error', '알 수 없는 오류')
    except Exception as e:
        return None, str(e)

# ----------------------
# 2. PUT 사용자 정보 수정
# ----------------------
#post form 요청 처리용 view(URL로 연결됨)
def update_user_address(request):
    if request.method == "POST":
        phone_prefix = request.POST.get("phone_prefix")
        phone_rest = request.POST.get("phone")
        phone = phone_prefix + phone_rest

        zipcode = request.POST.get("zipcode")
        address_name = request.POST.get("address_name")
        address_detail = request.POST.get("address_detail")
        address_name = request.POST.get("address_name", "")
        full_address = f"({zipcode}) {address_name} {address_detail}"

        success, error = update_user_info(
            request=request,
            name=request.user.first_name,
            email=request.user.email,
            phone=phone,
            address=full_address
        )

        if success:
            messages.success(request, "주소가 성공적으로 변경되었습니다.")
        else:
            messages.error(request, f"주소 변경 실패: {error}")

        return redirect("profile")
    
    profile_data, error = fetch_user_info(request)

    print("📥 fetch_user_info 결과:", profile_data)
    
    return render(request, "accounts/user_info.html", {
        "user": request.user,
        "profile": profile_data,
        "active_tab": "profile"
    })

@csrf_exempt
def update_profile_api(request):
    if request.method != "POST":
        print("❌ 잘못된 HTTP 메서드:", request.method)
        return JsonResponse({"error": "Invalid method"}, status=405)

    print("📥 요청 수신 - 헤더:", dict(request.headers))
    print("📥 요청 수신 - 본문(raw):", request.body)

    try:
        data = json.loads(request.body)
        phone = data.get("phone")
        address = data.get("address")
        print("📦 파싱된 데이터:", data)
    except Exception as e:
        print("❌ JSON 파싱 오류:", str(e))
        return JsonResponse({"error": "데이터 파싱 실패"}, status=400)

    token = get_jwt_from_session(request)
    if not token:
        print("🔐 JWT 토큰 없음 (세션에 없음)")
        return JsonResponse({"error": "로그인 필요"}, status=401)

    print("🔑 JWT 추출 성공:", token)
    print("📨 수정 요청 내용 → phone:", phone, "address:", address)

    # 내부 위임 로직
    success, error = update_user_info(request, name=None, email=None, phone=phone, address=address)

    if success:
        print("✅ 사용자 정보 수정 성공")
        return JsonResponse({"success": True})
    else:
        print("❌ 사용자 정보 수정 실패:", error)
        return JsonResponse({"error": error}, status=400)

#로직 처리용 (SSO API와 통신)
def update_user_info(request, name, email, phone, address):
    token = get_jwt_from_session(request)
    print("🐍 access_token:", token)

    if not token:
        return False, 'JWT 토큰이 없습니다.'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'name': name,
        'email': email,
        'phone': phone,
        'address': address
    }
    try:
        res = requests.put(f'{SSO_API_BASE}/user-info/', json=payload, headers=headers)
        if res.status_code == 200:
            return True, None
        return False, res.json().get('error', '알 수 없는 오류')
    except Exception as e:
        return False, str(e)

# ----------------------
# 3. PUT 비밀번호 변경
# ----------------------

def change_user_password(request):
    if request.method == "POST":
        token = get_jwt_from_session(request)
        if not token:
            messages.error(request, "로그인이 필요합니다.")
            return redirect("profile")

        current_pw = request.POST.get("current_pw")
        new_pw = request.POST.get("new_pw")
        confirm_pw = request.POST.get("confirm_pw")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "current_pw": current_pw,
            "new_pw": new_pw,
            "confirm_pw": confirm_pw
        }

        try:
            res = requests.put("http://localhost:8001/api/change-password/", json=payload, headers=headers)
            if res.status_code == 200:
                data = res.json()
                if data.get("force_logout"):
                    request.session.flush()
                    return render(request, "accounts/user_info.html", {
                        "force_logout": True,
                        "profile": {},
                        "active_tab": "password"
                    })
                else:
                    messages.success(request, "비밀번호가 변경되었습니다.")
                    return redirect("profile")
            else:
                error_msg = res.json().get("error", "비밀번호 변경 실패")
                messages.error(request, error_msg)  # ✅ 메시지로 출력!
        except Exception as e:
            messages.error(request, f"에러 발생: {str(e)}")

    return render(request, "accounts/user_info.html", {
        "active_tab": "password"
    })

# --------------------------
# ✅ 쪽지함 / 일정관리
# --------------------------

@permission_classes([IsAuthenticated])
def message_box(request):
    return render(request, 'accounts/message_box.html')


@permission_classes([IsAuthenticated])
def todo_page(request):
    return render(request, 'accounts/todo.html')