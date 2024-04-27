from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class StoredPassword(models.Model):
    class ComplexityLevel(models.TextChoices):
        '''Defines complexity levels for stored passwords.'''
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    user = models.ForeignKey(User, related_name='passwords', on_delete=models.CASCADE)
    title = models.CharField(max_length=155)
    notes = models.TextField(blank=True)
    password = models.CharField(max_length=128)
    complexity_level = models.CharField(max_length=10, choices=ComplexityLevel.choices, default=ComplexityLevel.LOW)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Password for user {self.user.first_name} {self.user.last_name} (created: {self.created_at})'
