from django.urls import path
from .views import baseInfo


urlpatterns = [
    path('base-info/', baseInfo.as_view(), name='base-info'),
]
