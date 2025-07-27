from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from smul.lecture.models import userLecture
from .models import EvalResult


def get_lecture_list_with_status(student_id, eval_type):
    lectures = userLecture.objects.filter(student_id=student_id)
    result = []

    for lec in lectures:
        submitted = EvalResult.objects.filter(
            student_id=student_id,
            course_code=lec.course_code,
            eval_type=eval_type
        ).exists()

        result.append({
            'id': lec.id,
            'course_code': lec.course_code,
            'course_name': lec.course_name,
            'professor': lec.professor,
            'credit': lec.credit,
            'is_submitted': submitted
        })
    return result


@login_required
def mid_evaluation(request):
    student_id = request.user.username
    lecture_list = get_lecture_list_with_status(student_id, 'mid')
    return render(request, 'evaluation/mid_evaluation.html', {'lectures': lecture_list})


@login_required
def final_evaluation(request):
    student_id = request.user.username
    lecture_list = get_lecture_list_with_status(student_id, 'final')
    return render(request, 'evaluation/final_evaluation.html', {'lectures': lecture_list})


@login_required
@require_http_methods(["GET", "POST"])
def mid_eval_form(request, lecture_id):
    return handle_eval_form(request, lecture_id, 'mid', 'mid_evaluation', 'evaluation/mid_eval_form.html')


@login_required
@require_http_methods(["GET", "POST"])
def final_eval_form(request, lecture_id):
    return handle_eval_form(request, lecture_id, 'final', 'final_evaluation', 'evaluation/final_eval_form.html')


def handle_eval_form(request, lecture_id, eval_type, redirect_view_name, template_name):
    lecture = get_object_or_404(userLecture, id=lecture_id, student_id=request.user.username)

    if request.method == "POST":
        score = request.POST.get('score')
        comment = request.POST.get('comment')

        EvalResult.objects.create(
            student_id=request.user.username,
            course_code=lecture.course_code,
            eval_type=eval_type,
            score=score,
            comment=comment,
        )

        return redirect(redirect_view_name)

    return render(request, template_name, {'lecture': lecture})
