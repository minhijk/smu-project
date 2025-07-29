from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .forms import ProfileUpdateForm, PasswordChangeForm
from .serializers import UserSerializer
from smul.academic.models import StudentProfile

# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# --------------------------
# ✅ 클라이언트 IP 추출
# --------------------------
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# --------------------------
# ✅ DRF API
# --------------------------

class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        user.first_name = request.data.get('name', user.first_name)
        user.email = request.data.get('email', user.email)
        user.save()

        try:
            profile = StudentProfile.objects.get(user=user)
            profile.phone = request.data.get('phone', profile.phone)
            profile.department = request.data.get('department', profile.department)
            profile.zipcode = request.data.get('zipcode', profile.zipcode)
            profile.address = request.data.get('address', profile.address)
            profile.address_detail = request.data.get('address_detail', profile.address_detail)
            profile.save()
        except StudentProfile.DoesNotExist:
            pass

        return Response({'message': '개인정보가 수정되었습니다.'})


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        current = request.data.get('current_password')
        new = request.data.get('new_password')
        confirm = request.data.get('confirm_password')

        if not request.user.check_password(current):
            return Response({'error': '현재 비밀번호가 일치하지 않습니다.'}, status=400)
        if new != confirm:
            return Response({'error': '새 비밀번호가 확인값과 다릅니다.'}, status=400)

        request.user.set_password(new)
        request.user.save()
        return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'})


# --------------------------
# ✅ 로그인 / 로그아웃
# --------------------------

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, '로그인 정보가 올바르지 않습니다.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# --------------------------
# ✅ 비밀번호 변경
# --------------------------

@login_required
def change_password(request):
    error_current = None
    error_confirm = None

    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            if not request.user.check_password(form.cleaned_data['current_password']):
                error_current = '현재 비밀번호가 틀렸습니다.'
            elif form.cleaned_data['new_password'] != form.cleaned_data['confirm_password']:
                error_confirm = '비밀번호 확인이 일치하지 않습니다.'
            else:
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                messages.success(request, '비밀번호가 변경되었습니다.')
                request.session['force_logout'] = True
                return redirect('user_info_page')
    else:
        form = PasswordChangeForm()

    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        profile = None

    ip_address = get_client_ip(request)
    last_login_time = request.user.last_login
    force_logout = request.session.get('force_logout', False)
    if force_logout:
        del request.session['force_logout']

    return render(request, 'accounts/user_info.html', {
        'user': request.user,
        'profile': profile,
        'ip_address': ip_address,
        'last_login_time': last_login_time,
        'password_form': form,
        'active_tab': 'password',
        'error_current': error_current,
        'error_confirm': error_confirm,
        'force_logout': force_logout,
    })


# --------------------------
# ✅ 개인정보 페이지
# --------------------------

@login_required
def user_info_page(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        profile = None

    ip_address = get_client_ip(request)
    last_login_time = request.user.last_login
    force_logout = request.session.get('force_logout', False)
    if force_logout:
        del request.session['force_logout']

    return render(request, 'accounts/user_info.html', {
        'user': request.user,
        'profile': profile,
        'ip_address': ip_address,
        'last_login_time': last_login_time,
        'force_logout': force_logout,
    })


@login_required
def update_user_address(request):
    if request.method == 'POST':
        try:
            profile = StudentProfile.objects.get(user=request.user)
            phone_prefix = request.POST.get('phone_prefix')
            phone_body = request.POST.get('phone')
            phone_full = f"{phone_prefix}{phone_body}"
            profile.phone = phone_full
            profile.zipcode = request.POST.get('zipcode')
            profile.address = request.POST.get('address')
            profile.address_detail = request.POST.get('address_detail')
            profile.save()
            messages.success(request, '개인 정보가 수정되었습니다.')
        except StudentProfile.DoesNotExist:
            messages.error(request, '학생 정보가 존재하지 않습니다.')
    return redirect('user_info_page')


# --------------------------
# ✅ 쪽지함 / 일정관리
# --------------------------

@login_required
def message_box(request):
    return render(request, 'accounts/message_box.html')


@login_required
def todo_page(request):
    return render(request, 'accounts/todo.html')
