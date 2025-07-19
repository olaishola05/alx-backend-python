from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, Conversation

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15)
    profile_photo = serializers.URLField(max_length=200)
    email = serializers.EmailField(required=True)
    is_online = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email']


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'message_body', 'sent_at', 'sender_name']


class ConversationSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['participants'].count() < 2:
            raise serializers.ValidationError("A conversation must include at least 2 participants.")
        return data

    class Meta:
        model = Conversation
        fields = '__all__'
