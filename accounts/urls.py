
from django.urls import path
from .views import RegisterAPIView,LoginAPIView,LogoutAPIView,LogoutAllAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns=[
    path("register/",RegisterAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
    path("logout-all/", LogoutAllAPIView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]

# Login
#   ↓
# Access Token + Refresh Token
#   ↓
# Access Token expires
#   ↓
# POST /api/accounts/token/refresh/
#   ↓
# Send Refresh Token
#   ↓
# SimpleJWT validates it
#   ↓
# New Access Token