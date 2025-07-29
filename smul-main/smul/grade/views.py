from django.shortcuts import render

# Create your views here.
def all_grade_sch(request):
    return render(request, 'grade/all_grade.html')