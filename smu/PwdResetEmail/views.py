from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils import timezone
from .models import EmailAuthCode
from .forms import EmailVerificationForm
from django.contrib import messages
import random

FAKE_USER_DB = {
    ('202321290', '강민서'): 'snrntpsy0629@naver.com',
    ('20240001', '김교수'): 'kim@smu.ac.kr'
}

def email_verification_view(request):
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        action = request.POST.get('action')

        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            name = form.cleaned_data['name']
            code_input = form.cleaned_data['code']
            email = FAKE_USER_DB.get((student_id, name))

            if not email:
                messages.error(request, '사용자 정보를 찾을 수 없습니다.')
                return render(request, 'email_auth/email_verification.html', {'form': form})

            if action == 'send':
                recent = EmailAuthCode.objects.filter(student_id=student_id, name=name).order_by('-created_at').first()
                if recent and not recent.is_re_request_blocked():
                    messages.error(request, '1분 후에 다시 요청해주세요.')
                else:
                    code = str(random.randint(100000, 999999))
                    EmailAuthCode.objects.create(student_id=student_id, name=name, email=email, code=code)
                    try:
                        send_mail(
                            '샘물 비밀번호 초기화 인증번호',
                            f'인증번호는 {code} 입니다.',
                            'noreply@smu.ac.kr',
                            [email],
                            fail_silently=False
                        )
                        messages.success(request, f'{email} 주소로 인증번호를 발송했습니다.')
                    except:
                        messages.error(request, '이메일 전송에 실패했습니다. 관리자에게 문의하세요.')

            elif action == 'confirm':
                latest = EmailAuthCode.objects.filter(student_id=student_id, name=name).order_by('-created_at').first()
                if latest and latest.code == code_input and not latest.is_expired():
                    latest.is_verified = True
                    latest.save()
                    messages.success(request, '✅ 이메일 인증이 완료되었습니다.')
                    return redirect('password_reset_form')
                else:
                    messages.error(request, '인증번호가 올바르지 않거나 만료되었습니다.')
    else:
        form = EmailVerificationForm()

    return render(request, 'PwdResetEmail/email_reset.html', {'form': form})

