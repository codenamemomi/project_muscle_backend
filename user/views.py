from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer, LoginSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings



User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not request.data or not any(request.data.values()):  # Check for empty input
            return Response({"error": "No input provided"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            response = Response(
                {"user": data["user"]}, status=status.HTTP_200_OK
            )

            response.set_cookie(
                key="refresh_token",
                value=data["refresh"],
                httponly=True,
                secure=True, 
                samesite="Lax", 
            )

            response.set_cookie(
                key="access_token",
                value=data["access"],
                httponly=True,
                secure=True,
                samesite="Lax",
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            raise AuthenticationFailed("No refresh token found in cookies.")

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
                new_refresh_token = str(refresh)
            else:
                new_refresh_token = refresh_token

        except Exception:
            raise AuthenticationFailed("Invalid or expired refresh token.")

        response = Response({"message": "Token refreshed"}, status=status.HTTP_200_OK)
        
        # Update cookies with new tokens
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return response

class LogoutView(APIView):
    def post(self, request):
        if 'refresh_token' in request.COOKIES:
            response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response
        return Response({"message": "No refresh token found in cookies."}, status=status.HTTP_400_BAD_REQUEST)

