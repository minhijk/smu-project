# dashboard/utils.py

#from jose import jwt
import jwt
from django.conf import settings

def decode_jwt(token):
    try:
        return jwt.decode(token, settings.PUBLIC_KEY, algorithms=["RS256"])
    except Exception:
        return None

def decode_jwt_from_request(request):
    token = request.session.get("access_token")
    if not token:
        return None
    try:
        return jwt.decode(token, settings.PUBLIC_KEY, algorithms=["RS256"])
    except Exception:
        return None

def get_jwt_from_session(request, token_name="access_token"):
    return request.session.get(token_name)
