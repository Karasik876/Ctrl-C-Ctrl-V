import uuid
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request

from backend import settings
from .serializers import *
from .models import *
from PIL import Image
import qrcode
import io
import boto3
import base64


class TestViewSet(viewsets.ModelViewSet):
    Test = Test

    def get_permissions(self):
        self.permission_classes = (IsAuthenticated,)
        return tuple(permission() for permission in self.permission_classes)

    def get_serializer_class(self):
        if self.action == 'create_post':
            self.serializer_class = TestCreateSerializer
        elif self.action == 'edit_get' or self.action == 'edit_post':
            self.serializer_class = TestEditSerializer
        self.serializer_class = TestDetailSerializer
        return self.serializer_class

    @action(detail=True)
    def create_post(self, request: Request, *args, **kwargs):
        data = request.data
        data['user_id'] = request.user.id
        data['the_class_id'] = 1

        im = Image.open('sheet.jpg')
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr_data = f'{data["questions"]};{data["choices"]};{data["answers"]}'
        qr.add_data(base64.b32encode(qr_data.encode()))
        qr.make(fit=True)

        im.paste(qr.make_image().resize((240, 240)), (656, 13))
        buffer = io.BytesIO()
        im.save(buffer, format='PNG')
        b_im = buffer.getvalue()

        session = boto3.session.Session()
        s3 = session.client(
            service_name='s3',
            endpoint_url='https://hb.ru-msk.vkcs.cloud/',
            aws_access_key_id=settings.AWS_ACCESS,
            aws_secret_access_key=settings.AWS_SECRET,
        )

        key = f'template_{request.user.id}_1_{uuid.uuid4()}.png'
        s3.put_object(Body=b_im, Bucket='digital-portfolio', Key=f'media/tests/{request.user.id}/{key}')

        data['template_img'] = f'https://digital-portfolio.hb.ru-msk.vkcs.cloud/media/tests/{request.user.id}/{key}'

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

    @action(detail=True)
    def edit_get(self, request: Request, *args, **kwargs):
        test = get_object_or_404(self.Test, pk=kwargs["id"])
        serializer = TestEditSerializer(test)
        return Response(serializer.data)

    @action(detail=True)
    def edit_post(self, request: Request, *args, **kwargs):
        test = get_object_or_404(self.Test, pk=kwargs["id"])
        if request.user.id:
            data = request.data
            serializer = TestEditSerializer(data=data, partial=True)
            if serializer.is_valid():
                serializer.update(instance=test, validated_data=data)
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(detail=True)
    def delete_class(self, request: Request, *args, **kwargs):
        test = get_object_or_404(self.Test, pk=kwargs["id"])
        test.delete()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True)
    def user_tests(self, request: Request, *args, **kwargs):
        tests = Test
        query = tests.objects.filter(user_id=request.user.id)
        serializer = TestDetailSerializer(query, many=True)
        return Response(serializer.data)