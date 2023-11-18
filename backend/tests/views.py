from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import *
from .models import *


class TestViewSet(viewsets.ModelViewSet):
    Test = Test

    def get_permissions(self):
        self.permission_classes = (IsAuthenticated,)
        return tuple(permission() for permission in self.permission_classes)

    @action(detail=True)
    def create_post(self, request: Request, *args, **kwargs):
        data = request.data
        data['user_id'] = int(request.user.id)
        serializer = TestCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def test_detail(self, request: Request, *args, **kwargs):
        test = get_object_or_404(self.Test, pk=kwargs['id'])
        serializer = TestDetailSerializer(test)
        return Response(serializer.data)
