from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,LoginSerializer,  LogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAPIView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()

        return Response(
            {
                "message":"User registered successfully",
                "user":{
                    "id":user.id,
                    "email":user.email
                }
            },
            status=status.HTTP_201_CREATED
        )

class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        return Response(
            {
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "email": user.email
                }
            },
            status=status.HTTP_200_OK
        )
class LoginAPIView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message":"Login Successfull",
                "user":{
                    "id":user.id,
                    "email":user.email,
                },
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }
            },
            status=status.HTTP_200_OK
        )

class LogoutAPIView(APIView):
        def post(self, request):
            serializer = LogoutSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(
                {
                    "message": "Logout successful"
                },
                status=status.HTTP_200_OK
            )

# POST /api/accounts/register/
#             ↓
#      RegisterSerializer
#             ↓
#       serializer.save()
#             ↓
#    User.objects.create_user()
#             ↓
#        UserManager
#             ↓
#       user.set_password()
#             ↓
#        Argon2 hashing
#             ↓
#         Database
# Password is stored as an Argon2 hash, not plaintext.

# Step 5.2 — Understand the two tokens

# When a user logs in successfully:

# Email + Password
#        ↓
#    Authenticate
#        ↓
#        ✓
#        ↓
#  ┌───────────────┐
#  │ JWT Generator │
#  └───────┬───────┘
#          ↓
#    ┌─────┴─────┐
#    ↓           ↓
# Access       Refresh
# Token        Token
#    ↓           ↓
# API calls    Get new
#              access token

# Access token

# Short-lived
# Sent with API requests
# Example:
# Authorization: Bearer <access_token>

# Refresh token

# Longer-lived
# Used to obtain a new access token
# Normally not sent with every API request

# 7.1 What is Refresh Token Rotation?

# Currently you have:

# Refresh Token A
#       ↓
# New Access Token

# And you can reuse Refresh Token A again:

# Refresh A → Access B
# Refresh A → Access C
# Refresh A → Access D

# With rotation, every successful refresh generates a new refresh token:

# Refresh A
#    ↓
# Access B + Refresh B
#              ↓
#         Refresh B
#              ↓
#         Access C + Refresh C

# So the old refresh token becomes invalid.

# This reduces the damage if a refresh token is stolen.

# 7.2 Enable Rotation

# Open:

# config/settings.py

# Add this:

# from datetime import timedelta

# Then add:

# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),

#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
# }

# So your configuration is essentially:

# Access Token
#     ↓
# 15 minutes

# Refresh Token
#     ↓
# 7 days

# Rotation
#     ↓
# Enabled

# Blacklist after rotation
#     ↓
# Enabled

# One important distinction

# Rotation and blacklisting are two different concepts:

# Feature	Purpose
# Rotation	Gives you a new refresh token
# Blacklisting	Makes the old refresh token unusable

# Logout from One Device
# User logs in on Laptop
#         ↓
# Refresh Token A

# User logs in on Phone
#         ↓
# Refresh Token B

# Logout from Laptop
#         ↓
# Blacklist Refresh Token A

# Laptop → ❌ Logged out
# Phone  → ✅ Still logged in
# We're logging out using the refresh token, not the access token.

# Why?

# Access token
#    ↓
# Short-lived
#    ↓
# Expires automatically

# Refresh token
#    ↓
# Long-lived
#    ↓
# Must be invalidated during logout