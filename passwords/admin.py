from django.contrib import admin

from passwords.models import StoredPassword


@admin.register(StoredPassword)
class StoredPasswordAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'complexity_level', 'created_at']
