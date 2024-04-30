from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from users.serializers import UserSerializer
from passwords.models import StoredPassword

User = get_user_model()


class StoredPasswordSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = StoredPassword
        fields = ['id', 'user', 'title', 'notes', 'password', 'complexity_level']
        read_only_fields = ['user']

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            validated_data['user'] = user
        password = validated_data.pop('password')
        instance = super().create(validated_data)
        instance.password = make_password(password)
        instance.save()
        return instance

    def validate(self, data):
        user = self.context.get('request').user
        title = data.get('title')

        if StoredPassword.objects.filter(user=user, title=title).exists():
            raise serializers.ValidationError('A password with this title already exists for the user.')

        return data
