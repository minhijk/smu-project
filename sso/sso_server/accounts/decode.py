import jwt
from django.conf import settings

def decode_jwt(token):  # ✅ token 문자열을 직접 받음
    try:
        return jwt.decode(token, settings.PUBLIC_KEY, algorithms=["RS256"])
    except jwt.ExpiredSignatureError:
        print("❌ JWT 만료")
        return None
    except jwt.InvalidTokenError as e:
        print("❌ JWT 디코딩 실패:", str(e))
        return None


