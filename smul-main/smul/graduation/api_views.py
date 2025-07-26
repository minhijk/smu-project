from django.http import JsonResponse
from .models import GraduationRequirement

def grad_credit_check(request):
    department = request.GET.get('department', '').strip()
    if department:
        results = GraduationRequirement.objects.filter(department__icontains=department)
    else:
        results = GraduationRequirement.objects.all()

    data = [{
        "college": row.college,
        "department": row.department,
        "entry_type": row.entry_type,
        "lib_req": row.lib_req,
        "lib_sel": row.lib_sel,
        "lib_total": row.lib_total,
        "major_core": row.major_core,
        "major_sel": row.major_sel,
        "major_total": row.major_total,
        "double_req": row.double_req,
        "double_sel": row.double_sel,
        "double_total": row.double_total,
        "sub_major1": row.sub_major1,
        "sub_major2": row.sub_major2,
        "remain_credit": row.remain_credit,
        "grad_avg": row.grad_avg,
        "gpa_grad": row.gpa_grad,
        "gpa_early": row.gpa_early
    } for row in results]

    return JsonResponse(data, safe=False)
