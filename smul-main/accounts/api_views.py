from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return Response({
        'id': user.username,   # 학번이라고 가정
        'name': user.first_name
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_info(request):
    user = request.user
    user.first_name = request.data.get('name', user.first_name)
    user.save()
    return Response({'message': '사용자 정보가 업데이트되었습니다.'})