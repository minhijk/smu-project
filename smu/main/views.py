from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from .models import Notice, Calendar
from django.contrib import messages

def home(request):
    notices = Notice.objects.order_by('-created_at')[:5]
    return render(request, 'main/index.html', {'notices': notices})

def notice_detail(request):
    notice_id = request.GET.get('id')
    notice = get_object_or_404(Notice, id=notice_id)
    return render(request, 'main/notice_detail.html', {'notice': notice})

def notice_list(request):
    notices = Notice.objects.order_by('-created_at')
    return render(request, 'main/notice_list.html', {'notices': notices})

def notice_search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Notice.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    return render(request, 'main/notice_search.html', {
        'query': query,
        'results': results,
    })

def academic_calendar(request):
    return render(request, 'main/academic/calendar.html')

def calendar_api(request):
    start = request.GET.get('start', '')[:10]  # YYYY-MM-DD 만 잘라서
    end = request.GET.get('end', '')[:10]

    print("start=", start, "end=", end)

    if start and end:
        events = Calendar.objects.filter(start_date__lte=end, end_date__gte=start)
    else:
        events = Calendar.objects.all()

    data = []
    for e in events:
        data.append({
            "title": e.title,
            "start": e.start_date.isoformat(),
            "end": e.end_date.isoformat() if e.end_date else None
        })
    return JsonResponse(data, safe=False)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home') 
        else:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')

    return render(request, 'main/login/login.html')

def logout(request):
    django_logout(request)
    return redirect('/')

def notice_filter_api(request):
    search_query = request.GET.get('q', '')
    category_name_filter = request.GET.get('category_name', '') 

    notices = Notice.objects.all()

    if category_name_filter:
        if category_name_filter == 'all':
            pass
        else:
            notices = notices.filter(category__name=category_name_filter)
    
    elif search_query:
        notices = notices.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )
            
    notices = notices.order_by('-created_at')[:10]

    result = [
        {
            'id': n.id,
            'title': n.title,
            'author': n.author.username if n.author else 'Unknown', 
            'created_at': n.created_at.strftime('%Y-%m-%d')
        }
        for n in notices
    ]
    return JsonResponse(result, safe=False)

def notice_search(request):
    search_query = request.GET.get('search', '') 
    category = request.GET.get('category', 'all')  
    notices = Notice.objects.all()

    if category != 'all':
        notices = notices.filter(category=category)

    if search_query:
        notices = notices.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )

    notices = notices.order_by('-created_at')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = list(notices.values('id', 'title', 'author__username', 'created_at'))
        for item in data:
            item['author'] = item.pop('author__username')
            item['created_at'] = item['created_at'].strftime('%Y-%m-%d')
        return JsonResponse(data, safe=False)

    return render(request, 'main/notice_search.html', {
        'query': search_query,
        'category': category,
        'results': notices,
    })