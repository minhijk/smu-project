from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import TotalGrade

@login_required
def total_grade_list_api(request):
    student_id = request.user.username  # 또는 request.user.student_id

    grades = TotalGrade.objects.filter(student_id=student_id).order_by('-year', '-semester')

    data = []
    for g in grades:
        data.append({
            'year': g.year,
            'semester': g.semester,
            'total_credit': g.total_credit,
            'grade_point': g.grade_point,
            'grade_average': g.grade_average,
            'percentile': g.percentile,
            'rank': g.rank,
        })

    return JsonResponse({'grades': data})
