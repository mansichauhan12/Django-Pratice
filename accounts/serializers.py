

from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


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