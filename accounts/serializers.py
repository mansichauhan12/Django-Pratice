

from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(
        write_only=True,
        min_length=8,
    )
    class Meta:
        model=User
        fields=["email","password"]

    def create(self,validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )


class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    def validate(self,data):
        email=data["email"]
        password=data["password"]
        user=authenticate(
            email=email,
            password=password
        )
        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )
        data["user"] = user
        return data
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, data):
         try:
             token = RefreshToken(data["refresh"])
             token.blacklist()
         except Exception:
                raise serializers.ValidationError(
                    "Invalid or expired refresh token."
                )
         return data

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True,
        min_length=8
    )
    def validate(self, data):
         try:
            uid=force_str(urlsafe_base64_decode(data["uid"]))
            user = User.objects.get(pk=uid)
         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                raise serializers.ValidationError(
                    "Invalid reset link."
                )
         if not default_token_generator.check_token(
            user,
            data["token"]
         ):
            raise serializers.ValidationError(
                "Invalid or expired reset link."
            )
         data["user"] = user
         return data
  


class VerifyEmailSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            uid = force_str(
                urlsafe_base64_decode(data["uid"])
            )

            user = User.objects.get(pk=uid)

        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist
        ):
            raise serializers.ValidationError(
                "Invalid verification link."
            )

        if user.is_email_verified:
            raise serializers.ValidationError(
                "Email is already verified."
            )

        if not default_token_generator.check_token(
            user,
            data["token"]
        ):
            raise serializers.ValidationError(
                "Invalid or expired verification link."
            )

        data["user"] = user

        return data

        
class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

# Yahan sabse important part:
# User.objects.create_user(...)

# Hum ye nahi karenge:

# User.objects.create(
#     email=...,
#     password=...
# )

# Because create() password ko automatically hash nahi karta.

# Instead:

# create_user()
#      ↓
# UserManager
#      ↓
# set_password(password)
#      ↓
# hashed password

# Aur tumhare UserManager mein already:

# user.set_password(password)

# hai.