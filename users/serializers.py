from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password

from django.core.validators import MinLengthValidator, RegexValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serilaizer for User Model
    """
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'profile_picture',
            'is_active',
        ]
        read_only_fields = ['is_active']


class RegisterSerializer(UserSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="User with that email already exists.")],
        error_messages={
            'unique': 'User with that email already exists.'
        }
    )
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                message='Password must contain at least eight characters, at least one uppercase letter , one number and one special character'
            ),
        ],
        error_messages={
            'blank': 'Password cannot be blank.',
            'required': 'Password is required.'
        }
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = super().create(validated_data)
        instance.password = make_password(password)
        instance.save()
        return instance


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        # Serialize the user
        user_data = UserSerializer(self.user).data

        data['user'] = user_data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
