from rest_framework import serializers
from .models import Test


class TestCreateSerializer(serializers.ModelSerializer):
    class Meta(serializers.SerializerMetaclass):
        model = Test
        fields = (
            'user_id',
            'test_name',
            'questions',
            'choices',
            'answers'
        )

    def create(self, validated_data):
        return Test.objects.create(**validated_data)


class TestDetailSerializer(serializers.ModelSerializer):
    class Meta(serializers.SerializerMetaclass):
        model = Test
        fields = '__all__'
