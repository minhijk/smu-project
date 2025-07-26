from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import userLecture

@login_required
def enrolled_lectures_api(request):
    student_id = request.user.username
    lectures = userLecture.objects.filter(student_id=student_id)

    data = []
    for lec in lectures:
        data.append({
            'course_code': lec.course_code,
            'course_name': lec.course_name,
            'credit': lec.credit,
            'semester': lec.semester,
            'day_time': lec.day_time,
            'professor': lec.professor,
        })

    return JsonResponse({'lectures': data})
