from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users.views import LoginViewSet, RegistrationViewSet, RefreshViewSet, UserViewSet
from passwords.views import StoredPasswordViewSet

routes = DefaultRouter()
routes.register(r'api/login', LoginViewSet, basename='auth-login')
routes.register(r'api/register', RegistrationViewSet, basename='auth-register')
routes.register(r'api/refresh', RefreshViewSet, basename='auth-refresh')

routes.register(r'api/users', UserViewSet, basename='users')
routes.register(r'api/passwords', StoredPasswordViewSet, basename='passwords')

urlpatterns = [
    path('admin/', admin.site.urls),
    *routes.urls,
]

if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
