from django.shortcuts import render

# Create your views here.

def grad_credit_sch(request):
    return render(request, 'graduation/grad_credit_sch.html')