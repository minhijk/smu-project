from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import CustomUser
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    student_id = serializers.CharField()

    def validate(self, attrs):
        student_id = attrs.get("student_id")
        password = attrs.get("password")

        user = CustomUser.objects.filter(student_id=student_id).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("학번 또는 비밀번호가 틀렸습니다.")

        # ✅ TokenObtainPairSerializer는 `self.username_field`를 기반으로 검증하므로
        # 강제로 attrs에 student_id를 username으로 넣어줌
        attrs["username"] = student_id
        attrs["password"] = password
        data = super().validate(attrs)
    
        # ✅ 토큰 외에 사용자 정보도 response에 포함되게끔
        data['name'] = user.full_name
        data['student_id'] = user.student_id
        data['role'] = user.role
        

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.full_name  # 사용자 정보 커스텀
        token['student_id'] = user.student_id
        token['role'] = user.role  # ✅ 역할 포함  # ✅ 관리자 여부 추가
        return token

    class Meta:
        fields = ("student_id", "password")

from rest_framework import serializers
from .models import CustomUser

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['student_id', 'full_name', 'email', 'phone', 'address']