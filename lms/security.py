import jwt
from datetime import datetime, timedelta
from django.conf import settings
from ninja.security import HttpBearer
from django.contrib.auth import get_user_model

User = get_user_model()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_jwt_token(user, token_type="access"):
    # Model user punya field role (admin, instructor, student)
    role = getattr(user, 'role', 'student') 
    
    if token_type == "access":
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
    payload = {
        "user_id": user.id,
        "role": role,
        "type": token_type,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != "access":
                return None
            
            user = User.objects.get(id=payload["user_id"])
            request.user_role = payload.get("role") # Nyimpen role di req untuk RBAC
            return user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return None

