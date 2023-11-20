from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import *
from .models import *


class ClassViewSet(viewsets.ModelViewSet):
    Class = Class

    def get_serializer_class(self):
        if self.action == 'create_post':
            return ClassCreateSerializer
        return ClassDetailSerializer

    def get_permissions(self):
        self.permission_classes = (IsAuthenticated,)
        return tuple(permission() for permission in self.permission_classes)

    @action(detail=True)
    def create_post(self, request: Request, *args, **kwargs):
        data = request.data
        data['user_id'] = request.user.id
        serializer = ClassCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def class_detail(self, request: Request, *args, **kwargs):
        the_class = get_object_or_404(self.Class, pk=kwargs['id'])
        serializer = ClassDetailSerializer(the_class)
        return Response(serializer.data)
