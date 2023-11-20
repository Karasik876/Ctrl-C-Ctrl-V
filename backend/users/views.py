from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()

    def get_permissions(self):
        if self.action == 'edit_get' or self.action == 'edit_post':
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (AllowAny,)
        return tuple(permission() for permission in self.permission_classes)

    def get_serializer_class(self):
        if self.action == 'edit_get' or self.action == 'edit_post':
            return UserEditSerializer
        return UserDetailSerializer

    @action(detail=True)
    def user_detail(self, request: Request, *args, **kwargs):
        user = get_object_or_404(self.User, pk=kwargs["id"])
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    @action(detail=True)
    def user_me(self, request: Request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = self.serializer_class(request.user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True)
    def edit_get(self, request: Request, *args, **kwargs):
        user = get_object_or_404(self.User, pk=kwargs["id"])
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    @action(detail=True)
    def edit_post(self, request: Request, *args, **kwargs):
        if request.user.id and kwargs['id'] == request.user.id:
            data = request.data
            serializer = self.serializer_class(data=data, partial=True)
            if serializer.is_valid():
                serializer.update(instance=request.user, validated_data=data)
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)






