from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'


class UserEditSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'first_name',
            'last_name',
        )


class UserDetailSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'is_superuser',
        )
