from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import *
from .models import *


class SheetViewSet(viewsets.ModelViewSet):
    Sheet = Sheet

    def get_permissions(self):
        self.permission_classes = (AllowAny,)
        return tuple(permission() for permission in self.permission_classes)

    def get_serializer_class(self):
        if self.action == 'create_post':
            return SheetCreateSerializer
        return SheetDetailSerializer

    @action(detail=True)
    def create_post(self, request: Request, *args, **kwargs):
        serializer = SheetCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def sheet_detail(self, request: Request, *args, **kwargs):
        test = get_object_or_404(self.Sheet, pk=kwargs['id'])
        serializer = SheetDetailSerializer(test)
        return Response(serializer.data)
