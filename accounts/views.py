from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,LoginSerializer,  LogoutSerializer,ForgotPasswordSerializer,ResetPasswordSerializer,VerifyEmailSerializer,ResendVerificationEmailSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import (OutstandingToken,BlacklistedToken)
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import User


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

        
class LogoutAllAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        tokens=OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        return Response(
            {
                "message": "Logged out from all devices successfully" 
            },
            status=status.HTTP_200_OK
        )

class ForgotPasswordAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user=User.objects.filter(
            email=email,
            is_active=True
        ).first()

        if user:
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            print("UID:", uid)
            print("TOKEN:", token)
            return Response(
            {
                "message": (
                    "If an account exists with this email, "
                    "a password reset link has been sent."
                )
            },
            status=status.HTTP_200_OK
        )

class ResetPasswordAPIView(APIView):
    def post(self, request):
      serializer=ResetPasswordSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      user = serializer.validated_data["user"]
      user.set_password(
            serializer.validated_data["new_password"]
        )
      user.save()
      return Response(
            {
                "message": "Password reset successful",
            },
            status=status.HTTP_200_OK
        )

class VerifyEmailAPIView(APIView):
    def post (self,request):
        serializer=VerifyEmailSerializer(
        data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data["user"]
        user.is_email_verified=True
        user.save(update_fields=["is_email_verified"])
        return Response(
            {
                "message":"Email verified successfully"
            },
            status=status.HTTP_200_OK
        )


class ResendVerificationEmailAPIView(APIView): 
    def post(self,request):
        serializer=ResendVerificationEmailSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        email=serializer.validated_data["email"]
        user=User.objects.filter(
            email=email,
            is_active=True,
        ).first()

        if user and not user.is_email_verified:
            uid=urlsafe_base64_encode(
                force_bytes(user.pk)

            )
            token=default_token_generator.make_token(
                user
            )
            print("uid",uid)
            print("token",token)
            return Response(
                {
                    "message":(
                              "If an unverified account exists "
                    "with this email, a verification "
                    "email has been sent."
                    )
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


# Great 👍 Step 10 — Logout from All Devices

# Now we need to solve a different problem.

# Suppose the user logged in from:

# Laptop  → Refresh Token A
# Phone   → Refresh Token B
# Tablet  → Refresh Token C

# If they choose "Logout from all devices", all three refresh tokens should become invalid:

# Refresh A → ❌
# Refresh B → ❌
# Refresh C → ❌
# 10.1 How will we do it?

# SimpleJWT's blacklist app keeps track of issued refresh tokens in:

# OutstandingToken

# So we'll find all outstanding tokens belonging to the current user and blacklist each one.






# Authentication System Walkthrough
# This document outlines the current state and implementation details of the JWT-based authentication, password reset, and email verification system in the accounts app.

# Data Models
# The system is built on a custom user model which overrides Django's default behavior to use email as the primary identifier instead of a username.

# User
# : The central model.

# email: EmailField (unique).
# is_email_verified: BooleanField (default False). Tracks whether the user has verified their email via the verification link.
# USERNAME_FIELD = "email"
# UserManager
# : Handles the creation of regular users and superusers, ensuring passwords are properly hashed using user.set_password().

# Core Authentication Flow (JWT)
# We use rest_framework_simplejwt to handle short-lived access tokens and long-lived refresh tokens.

# Endpoints
# Register (POST /api/accounts/register/): Takes email and password. Creates an unverified user.
# Login (POST /api/accounts/login/): Authenticates credentials and returns a payload containing access and refresh tokens.
# Token Refresh (POST /api/accounts/token/refresh/): Accepts a valid refresh token and returns a new access token.
# Logout (POST /api/accounts/logout/): Accepts a refresh token and blacklists it, ending the session on that specific device.
# Logout All (POST /api/accounts/logout-all/): Requires authentication. Finds all OutstandingTokens for the user and blacklists them, logging the user out of all devices.
# Secure Link Mechanisms (Tokens & UIDs)
# For actions like password resets and email verifications, the system sends secure, one-time-use links. These links consist of two parts:

# uid: The base64 encoded user ID (urlsafe_base64_encode(force_bytes(user.pk))).
# token: A cryptographic hash generated by default_token_generator.make_token(user).
# Password Reset Workflow
# Forgot Password (POST /api/accounts/forgot-password/):
# Input: User's email.
# Process: Looks up the user. If found, generates a uid and token. (Currently printed to the console for testing; eventually to be sent via email).
# Reset Password (POST /api/accounts/reset-password/):
# Input: uid, token, and new_password.
# Process: Validates the uid by decoding it and fetching the user. Validates the token. If valid, updates the user's password using user.set_password(), inherently invalidating the token from future use.
# Email Verification Workflow
# Resend Verification Email (POST /api/accounts/resend-verification-email/):
# Input: User's email.
# Process: If the user exists and is not already verified, generates a uid and token. (Currently printed to the console).
# Verify Email (POST /api/accounts/verify-email/):
# Input: uid and token (usually appended to a URL parameter on the frontend).
# Process: Decodes uid and validates the token. Updates the user's is_email_verified field to True using user.save(update_fields=["is_email_verified"]).