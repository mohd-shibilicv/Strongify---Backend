from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from passwords.serializers import StoredPasswordSerializer
from passwords.models import StoredPassword


class StoredPasswordViewSet(ModelViewSet):
    serializer_class = StoredPasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = StoredPassword.objects.filter(user=self.request.user)
        return queryset.order_by('-created_at')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id
        return context
