from django.urls import path, include
from .views import (ConversationViewSet, MessageViewSet, AdminUserListViewSet)
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'admin/users', AdminUserListViewSet, basename='admin-users')

# Nested router for messages under conversations
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# urlpatterns = [
    # path('', include(router.urls)),
    # path('', include(conversation_router.urls)),
# ]
# 

urlpatterns = router.urls + conversation_router.urls