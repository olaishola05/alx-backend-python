from django.urls import path, include
from .views import (ConversationViewSet, MessageViewSet)
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
