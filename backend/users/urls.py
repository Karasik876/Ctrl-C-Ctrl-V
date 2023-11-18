from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views
from djoser.views import UserViewSet

urlpatterns = [
    path("users/<int:id>/edit", views.UserViewSet.as_view({"get": "edit_get", "post": "edit_post"}), name="edit"),
    path("users/detail/<int:id>/", views.UserViewSet.as_view({"get": "user_detail"}), name="user_detail"),
    path("users/me/", views.UserViewSet.as_view({"get": "user_me"}), name="user_me"),
    path('users/auth/signup', UserViewSet.as_view({'post': 'create'}), name="register"),
    path("users/auth/signin", TokenObtainPairView.as_view(), name="create-token"),
    path("users/auth/refresh", TokenRefreshView.as_view(), name="refresh-token"),
    path("users/auth/verify", TokenVerifyView.as_view(), name="verify-token"),
    path("users/activation/resend-activation/", UserViewSet.as_view({"post": "resend_activation"}), name="resend_activation"),
    path("users/activation/activate/<str:uid>/<str:token>", UserViewSet.as_view({"post": "activation"}), name="activate"),
    path("users/reset/reset-password/", UserViewSet.as_view({"post": "reset_password"}), name="reset_password"),
    path("users/reset/reset-password-confirm/<str:uid>/<str:token>/", UserViewSet.as_view({"post": "reset_password_confirm"}),
         name="reset_password_confirm"),
    path("users/reset/reset-email", UserViewSet.as_view({"post": "reset_username"}), name="reset_email"),
    path("users/reset/reset-email-confirm/<str:uid>/<str:token>", UserViewSet.as_view({"post": "reset_username_confirm"}), name="reset_email_confirm"),
]