from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def enrollment_page(request):
    return render(request, 'lecture/enrollment.html')
