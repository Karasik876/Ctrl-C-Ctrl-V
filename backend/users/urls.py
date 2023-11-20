from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views
from djoser.views import UserViewSet

urlpatterns = [
    path("edit/<int:id>", views.UserViewSet.as_view({"get": "edit_get", "post": "edit_post"}), name="edit"),
    path("detail/<int:id>/", views.UserViewSet.as_view({"get": "user_detail"}), name="user_detail"),
    path("me/", views.UserViewSet.as_view({"get": "user_me"}), name="user_me"),
    path('auth/signup', UserViewSet.as_view({'post': 'create'}), name="register"),
    path("auth/signin", TokenObtainPairView.as_view(), name="create-token"),
    path("auth/refresh", TokenRefreshView.as_view(), name="refresh-token"),
    path("auth/verify", TokenVerifyView.as_view(), name="verify-token"),
    path("activation/resend-activation/", UserViewSet.as_view({"post": "resend_activation"}), name="resend_activation"),
    path("activation/activate/<str:uid>/<str:token>", UserViewSet.as_view({"post": "activation"}), name="activate"),
    path("reset/reset-password/", UserViewSet.as_view({"post": "reset_password"}), name="reset_password"),
    path("reset/reset-password-confirm/<str:uid>/<str:token>/", UserViewSet.as_view({"post": "reset_password_confirm"}),
         name="reset_password_confirm"),
    path("reset/reset-email", UserViewSet.as_view({"post": "reset_username"}), name="reset_email"),
    path("reset/reset-email-confirm/<str:uid>/<str:token>", UserViewSet.as_view({"post": "reset_username_confirm"}), name="reset_email_confirm"),
]