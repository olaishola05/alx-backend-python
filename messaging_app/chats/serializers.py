from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, Conversation
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token payload
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['user_id'] = str(user.user_id)

        # Add custom user profile data if you have a profile model
        if hasattr(user, 'profile'):
            token['profile_id'] = user.profile.id
            token['full_name'] = user.profile.full_name

        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except serializers.ValidationError as exc:
            raise serializers.ValidationError(
                {'detail': 'Invalid credentials. Please check your username and password.'}
                )
        except Exception as e:
            raise serializers.ValidationError(
                {
                    "details": str(e)
                }
            ) 

        # Add extra response data
        assert self.user is not None, "User must be authenticated to obtain token."
        data.update({
            'user_id': self.user.user_id, # type: ignore
            'username': self.user.username,
            'email': self.user.email,
            'is_staff': self.user.is_staff,
        }) # type: ignore

        # Add user permissions
        # data['permissions'] = list(self.user.get_all_permissions())

        # Add user groups
        # data['groups'] = [group.name for group in self.user.groups.all()]

        return data

class WelcomeSerializer(serializers.Serializer):
    welcome_message = serializers.CharField(default="Welcome to the Messaging App API!")
    available_routes = serializers.ListField(
        child=serializers.CharField(),
        default=[
            "GET /api/v1/conversations/",
            "POST /api/v1/conversations/",
            "GET /api/v1/conversations/{conversation_id}/",
            "GET /api/v1/conversations/{conversation_id}/messages/",
            "POST /api/v1/conversations/{conversation_id}/messages/"
        ]
    )
class UserRegisterSerializer(serializers.ModelSerializer):
    """
    User registration with password confirmation
    """
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'user_id']
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password don't match")
        return attrs
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email already exists')
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user
  
class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15)
    profile_photo = serializers.URLField(max_length=200)
    email = serializers.EmailField(required=True)
    is_online = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email']
        read_only_fields = ['user_id', 'date_joined']


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'message_body', 'sent_at', 'sender_name']
        read_only_fields = ['sender']


class ConversationSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['participants'].count() < 2:
            raise serializers.ValidationError("A conversation must include at least 2 participants.")
        return attrs

    class Meta:
        model = Conversation
        fields = '__all__'
