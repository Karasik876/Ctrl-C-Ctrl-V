from rest_framework import serializers
from .models import Class


class ClassCreateSerializer(serializers.ModelSerializer):
    class Meta(serializers.SerializerMetaclass):
        model = Class
        fields = (
            'user_id',
            'class_name',
            'class_number',
            'class_letter',
        )

    def create(self, validated_data):
        return Class.objects.create(**validated_data)


class ClassDetailSerializer(serializers.ModelSerializer):
    class Meta(serializers.SerializerMetaclass):
        model = Class
        fields = '__all__'
