from rest_framework import serializers
from .models import Sheet


class SheetCreateSerializer(serializers.ModelSerializer):
    class Meta(serializers.SerializerMetaclass):
        model = Sheet
        fields = (
            'user_id',
            'test_id',
            'the_class_id',
            'name_image',
            'sheet_image',
            'student_answers',
            'result'
        )

    def create(self, validated_data):
        return Sheet.objects.create(**validated_data)


class SheetDetailSerializer(serializers.ModelSerializer):
    class Meta(serializers.SerializerMetaclass):
        model = Sheet
        fields = '__all__'
