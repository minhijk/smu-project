from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from .forms import ProfileUpdateForm, PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm

# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer  # ← serializers.py에 맞게 import

# ✅ REST API: 사용자 정보 조회
class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# ✅ REST API: 사용자 정보 수정
class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        user.first_name = request.data.get('name', user.first_name)
        user.save()
        return Response({'message': '정보가 수정되었습니다.'})

# ✅ 로그인
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')  # 홈 뷰 이름에 맞게 변경
        else:
            messages.error(request, '로그인 정보가 올바르지 않습니다.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# ✅ 로그아웃
def logout_view(request):
    logout(request)
    return redirect('login')

# ✅ 개인정보 수정
@login_required
def profile_update(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, '정보가 수정되었습니다.')
            return redirect('profile_update')
    else:
        profile_form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile_update.html', {
        'profile_form': profile_form,
        'active_tab': 'profile'
    })

# ✅ 비밀번호 변경
@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            if not request.user.check_password(form.cleaned_data['current_password']):
                messages.error(request, '현재 비밀번호가 틀렸습니다.')
            elif form.cleaned_data['new_password'] != form.cleaned_data['confirm_password']:
                messages.error(request, '비밀번호 확인이 일치하지 않습니다.')
            else:
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, '비밀번호가 변경되었습니다.')
                return redirect('password_change')
    else:
        form = PasswordChangeForm()

    return render(request, 'accounts/profile_update.html', {
        'password_form': form,
        'active_tab': 'password'
    })
@login_required
def user_profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def user_profile_view(request):
    return render(request, 'accounts/profile_edit.html')


@login_required
def user_info_page(request):
    return render(request, 'accounts/user_info.html')

@login_required
def user_info_page(request):
    return render(request, 'accounts/user_info.html', {'user': request.user})