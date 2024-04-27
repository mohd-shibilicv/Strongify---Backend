from django.urls import path

from passwords import views


app_name = 'passwords'
urlpatterns = [
    path('', views.TestView.as_view(), name='test-view'),
]
