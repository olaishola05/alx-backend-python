from .models import Conversation, Message, User
from .serializers import ConversationSerializer, CustomTokenObtainPairSerializer, MessageSerializer, WelcomeSerializer, UserRegisterSerializer, UserSerializer
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAuthenticatedOrReadOnly, IsParticipantOfConversation
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .pagination import MessagePagination
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend
class WelcomeViewSet(viewsets.ViewSet):
    """
    API endpoint to get a welcome message and available routes.
    """
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        serializer = WelcomeSerializer({})
        return Response(serializer.data, status=status.HTTP_200_OK)
      
class UserRegistrationView(viewsets.ModelViewSet):
  """
  Custom viiew to register new user
  """
  queryset = User.objects.all()
  permission_classes = [permissions.AllowAny]
  serializer_class = UserRegisterSerializer
  http_method_names = ['post']
  
  def create(self, request, *args, **kwargs):
    try:
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      user = serializer.save()
      serialized_user = UserRegisterSerializer(user)
      return Response({
        "message": "Registeration successful",
        "user": serialized_user.data,
      }, status=status.HTTP_201_CREATED)
    except serializers.ValidationError as ve:
      return Response({
                "message": "Validation failed.",
                "errors": ve.detail
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      return Response({
                "message": "An unexpected error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom view to obtain JWT tokens with additional user information.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get tokens from serializer
        token_data = serializer.validated_data
        access_token = token_data.get("access")
        refresh_token = token_data.get("refresh")

        # Prepare response
        response = Response(token_data, status=status.HTTP_200_OK)

        # Attach access token to header
        response["Authorization"] = f"Bearer {access_token}"

        return response
    
    
class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint to get all conversations
    """
    queryset = Conversation.objects.all().order_by('created_at')
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthenticatedOrReadOnly]
    
    def get_queryset(self): # type: ignore
        return self.queryset.filter(participants=self.request.user)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'participants__username']
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint to get all the Messages
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filter_class = MessageFilter
    
    def get_queryset(self): # type: ignore
        if not self.request.user or not self.request.user.is_authenticated:
          raise PermissionDenied("You are not allowed to perform this action.")

        user = self.request.user
        return Message.objects.filter(conversation__participants=user)

    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_pk']
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not part of this conversation")
        serializer.save(sender=self.request.user, conversation=conversation)
        
    def perform_update(self, serializer):
        if self.get_object().sender != self.request.user:
            raise PermissionDenied("You can only edit your own message")
        serializer.save()
        
    def perform_destroy(self, instance):
        if instance.sender != self.request.user:
            raise PermissionDenied("You can only delete your own messages")
        instance.delete()

class AdminUserListViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]