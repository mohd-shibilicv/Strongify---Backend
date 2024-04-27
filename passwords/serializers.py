from rest_framework import serializers

from users.serializers import UserSerializer
from passwords.models import StoredPassword


class StoredPasswordSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StoredPassword
        fields = [
            'id',
            'user',
            'notes',
            'password',
            'complexity_level'
        ]
