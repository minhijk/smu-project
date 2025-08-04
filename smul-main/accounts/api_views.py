from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from smul.utils import decode_jwt_from_request

@api_view(['GET'])
@permission_classes([AllowAny])  # 🔄 모든 요청 허용 후 내부에서 판단
def get_user_info(request):
    if request.user.is_authenticated:
        return Response({
            'id': request.user.username,
            'name': request.user.first_name
        })

    # JWT로 로그인 여부 확인
    payload = decode_jwt_from_request(request)
    if not payload:
        return Response({'error': 'unauthorized'}, status=401)

    return Response({
        'id': payload.get("student_id"),
        'name': payload.get("name")
    })


@api_view(['PUT'])
@permission_classes([AllowAny])  # 이 부분도 세션 사용자만 수정 가능하게 조정
def update_user_info(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        # JWT 사용자도 허용
        payload = decode_jwt_from_request(request)
        if not payload:
            return Response({'error': 'unauthorized'}, status=401)
        try:
            user = User.objects.get(username=payload['student_id'])
        except User.DoesNotExist:
            return Response({'error': '사용자를 찾을 수 없습니다.'}, status=404)

    user.first_name = request.data.get('name', user.first_name)
    user.save()
    return Response({'message': '사용자 정보가 업데이트되었습니다.'})
