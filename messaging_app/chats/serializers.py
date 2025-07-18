from rest_framework import serializers
from django.contrib.auth import get_user_model
from models import Message, Conversation, User

# User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email']


class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.UUIDField(source='sender.user_id', read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = serializers.SlugRelatedField(slug_field='user_id', many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']