from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as django_logout
from django.contrib import messages
from django.http import HttpResponse

def password_reset(request):
    return render(request, 'login/password_reset.html')

from django.http import HttpResponse

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return HttpResponse("""
                <script>
                    opener.location.reload();  // 부모창 새로고침
                    window.close();            // 팝업창 닫기
                </script>
            """)
        else:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')

    return render(request, 'login/login.html')


def logout(request):
    django_logout(request)
    return redirect('/')