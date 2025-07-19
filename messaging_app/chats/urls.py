from django.urls import path
from .views import (ConversationViewSet, MessageViewSet)

conversation_list = ConversationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

message_list = MessageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('conversations/', conversation_list, name='conversation-list'),
    path('messages/', message_list, name='message-list'),
]
