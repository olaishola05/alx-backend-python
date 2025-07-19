from django.urls import path, include
from .views import (ConversationViewSet, MessageViewSet, root_welcome)
# from rest_framework import routers
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under conversations
conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# urlpatterns = [
#     path('', root_welcome, name='root-welcome'),
#     path('', include(router.urls)),
#     path('', include(conversation_router.urls)),
# ]

urlpatterns = [
    path('', root_welcome, name='root-welcome'),  # ✅ This is now exclusive for the homepage
    path('api/', include(router.urls)),           # ✅ All API endpoints go under /api/
    path('api/', include(conversation_router.urls)),
]
