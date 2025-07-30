import jwt
from django.conf import settings

def decode_jwt_from_request(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token,
                settings.SIMPLE_JWT["VERIFYING_KEY"],
                algorithms=["RS256"]
            )
            return payload
        except jwt.ExpiredSignatureError:
            print("⚠️ 토큰 만료됨")
        except jwt.InvalidTokenError as e:
            print("❌ 잘못된 토큰:", e)
    return None
