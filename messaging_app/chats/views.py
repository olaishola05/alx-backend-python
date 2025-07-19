from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def root_welcome(request):
    return Response({
        "message": "Welcome to the Messaging API 👋",
        "available_routes": {
            "Conversations": "/api/conversations/",
            "Messages": "/api/conversations/<conversation_id>/messages/"
        }
    })


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint to get all conversations
    """
    queryset = Conversation.objects.all().order_by('created_at')
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show conversations the current user is a part of
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint to get all the Messages
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
