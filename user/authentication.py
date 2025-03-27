from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header_token = super().authenticate(request)
        if header_token:
            return header_token  # Returns (user, token)

        access_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE'))

        if access_token:
            validated_token = self.get_validated_token(access_token)
            user = self.get_user(validated_token)
            return (user, validated_token)  # ✅ MUST RETURN A TUPLE

        return None  # No authentication
