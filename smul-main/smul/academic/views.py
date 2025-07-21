from django.shortcuts import render

# Create your views here.
def profile_update(request):
    return render(request, 'academic/profile_update.html')

def schAltAply(request):
    return render(request, 'academic/schAltAply.html')