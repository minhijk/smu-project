from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# GET용 (이름 조회 등)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name']  # 필요한 필드 선택
