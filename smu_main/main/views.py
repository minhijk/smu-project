from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .models import Notice, AcademicEvent

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
    

def academic_calendar(request):
    return render(request, 'main/academic/calendar.html')

from django.http import JsonResponse
from .models import AcademicEvent

def calendar_api(request):
    start = request.GET.get('start', '')[:10]  # YYYY-MM-DD
    end = request.GET.get('end', '')[:10]

    print("start=", start, "end=", end)

    if start and end:
        events = AcademicEvent.objects.filter(start__lte=end, end__gte=start)
    else:
        events = AcademicEvent.objects.all()

    data = []
    for e in events:
        data.append({
            "id": e.id,
            "title": e.title,
            "start": e.start.isoformat(),
            "end": e.end.isoformat() if e.end else None,
        })
    return JsonResponse(data, safe=False)


from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout

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

# 공지사항 수정 API
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .utils import decode_jwt_from_request
import json

@csrf_exempt
@require_http_methods(["POST"])
def update_notice(request):
    payload = decode_jwt_from_request(request)
    if not payload or payload.get("role") != "admin":
        return JsonResponse({"error": "관리자 권한이 없습니다."}, status=403)

    try:
        data = json.loads(request.body)
        notice_id = data.get("id")
        new_title = data.get("title")
        new_content = data.get("content")

        notice = Notice.objects.get(id=notice_id)
        notice.title = new_title
        notice.content = new_content
        notice.save()

        return JsonResponse({"message": "공지사항이 수정되었습니다."})
    except Notice.DoesNotExist:
        return JsonResponse({"error": "해당 공지사항이 존재하지 않습니다."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# 공지작성 api
from django.contrib.auth.models import User  # 작성자 정보 매핑용
from .models import Notice

@csrf_exempt
@require_http_methods(["POST"])
def create_notice(request):
    payload = decode_jwt_from_request(request)
    print("📦 payload =", payload)  # 디버깅용

    if not payload:
        return JsonResponse({"error": "토큰이 없거나 유효하지 않습니다."}, status=403)

    if payload.get("role") != "admin":
        return JsonResponse({"error": "관리자만 공지를 작성할 수 있습니다."}, status=403)

    try:
        data = json.loads(request.body)
        title = data.get("title")
        content = data.get("content")
        category = data.get("category")

        author = payload.get("name", "Unknown")  # ✅ name은 CustomUser.full_name

        notice = Notice.objects.create(
            title=title,
            content=content,
            category=category,
            author=author
        )

        return JsonResponse({"message": "공지사항이 등록되었습니다.", "id": notice.id}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

#공지삭제 api
@csrf_exempt
@require_http_methods(["POST"])
def delete_notice(request):
    payload = decode_jwt_from_request(request)
    if not payload or payload.get("role") != "admin":
        return JsonResponse({"error": "관리자만 공지를 삭제할 수 있습니다."}, status=403)

    try:
        data = json.loads(request.body)
        notice_id = data.get("id")

        notice = Notice.objects.get(id=notice_id)
        notice.delete()

        return JsonResponse({"message": "공지사항이 삭제되었습니다."}, status=200)
    except Notice.DoesNotExist:
        return JsonResponse({"error": "공지사항을 찾을 수 없습니다."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def notice_create_page(request):
    return render(request, "main/notice_create.html")

from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AcademicEvent
from .serializers import AcademicEventSerializer
from .utils import decode_jwt_from_request

#달력
@api_view(["POST"])
def create_event(request):
    payload = decode_jwt_from_request(request)
    if not payload or payload.get("role") != "admin":
        return Response({"error": "관리자만 등록할 수 있습니다."}, status=403)

    serializer = AcademicEventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(["PUT"])
def update_event(request, pk):
    payload = decode_jwt_from_request(request)
    if not payload or payload.get("role") != "admin":
        return Response({"error": "관리자만 수정할 수 있습니다."}, status=403)

    try:
        event = AcademicEvent.objects.get(pk=pk)
    except AcademicEvent.DoesNotExist:
        return Response({"error": "해당 이벤트가 존재하지 않습니다."}, status=404)

    serializer = AcademicEventSerializer(event, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(["DELETE"])
def delete_event(request, pk):
    payload = decode_jwt_from_request(request)
    if not payload or payload.get("role") != "admin":
        return Response({"error": "관리자만 삭제할 수 있습니다."}, status=403)

    try:
        event = AcademicEvent.objects.get(pk=pk)
        event.delete()
        return Response(status=204)
    except AcademicEvent.DoesNotExist:
        return Response({"error": "해당 이벤트가 존재하지 않습니다."}, status=404)