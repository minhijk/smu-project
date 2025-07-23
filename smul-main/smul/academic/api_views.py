from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .models import StudentProfile, LeaveRequest

# ✅ 사용자 정보 조회
@login_required
def get_user_info(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
        data = {
            'student_id': profile.student_id,
            'name': profile.name,
            'gender': profile.gender,
            'department': profile.department,
            'nationality': profile.nationality,
            'phone': profile.phone,
            'email': profile.email,
            'professor': profile.professor,
            'eng_name': profile.eng_name,
            'bank': profile.bank,
            'account_number': profile.account_number,
            'account_holder': profile.account_holder,
        }
        return JsonResponse(data)
    except StudentProfile.DoesNotExist:
        return JsonResponse({'error': '프로필이 존재하지 않습니다.'}, status=404)

# ✅ 사용자 정보 수정
@login_required
@require_http_methods(["PUT"])
def update_user_info(request):
    try:
        data = json.loads(request.body)
        profile = StudentProfile.objects.get(user=request.user)

        profile.phone = data.get('phone', profile.phone)
        profile.email = data.get('email', profile.email)
        profile.eng_name = data.get('eng_name', profile.eng_name)
        profile.bank = data.get('bank', profile.bank)
        profile.account_number = data.get('account_number', profile.account_number)
        profile.account_holder = data.get('account_holder', profile.account_holder)
        profile.save()

        return JsonResponse({'status': 'updated'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# ✅ 휴학/복학/자퇴 신청 처리
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def apply_leave(request):
    try:
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        status = request.POST.get('status')
        document = request.FILES.get('document')

        if not all([student_id, name, status, document]):
            return JsonResponse({'error': '모든 필드를 입력해주세요.'}, status=400)

        LeaveRequest.objects.create(
            user=request.user,
            student_id=student_id,
            name=name,
            status=status,
            document=document
        )

        return JsonResponse({'status': '신청 완료'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)