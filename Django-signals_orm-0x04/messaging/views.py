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
from rest_framework.decorators import action
from .utils import build_threaded_messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class WelcomeViewSet(viewsets.ViewSet):
    """
    API endpoint to get a welcome message and available routes.
    """
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        serializer = WelcomeSerializer({})
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ViewSet):
  queryset = User.objects.all()
  serializer = UserSerializer
  permission_classes = [permissions.IsAuthenticated]
  
  def get_permissions(self):
     
     if self.action == 'list':
       permission_classes = [permissions.IsAdminUser]
     elif self.action == 'retrieve':
       permission_classes = [permissions.IsAuthenticated]
     elif self.action == 'destroy':
       permission_classes = [permissions.IsAdminUser]
     else:
       permission_classes = [permissions.IsAuthenticated]
     return [permission() for permission in permission_classes]
 
  @action(detail=True, methods=['delete'])
  def delete_user(self, request, pk=None):
      """
        Allows an authenticated user to delete their own account.
      """
      
      user = self.get_object() # type: ignore
      if user != request.user:
          return Response(
              {"detail": "You do not have permission to delete this account"},
              status=status.HTTP_403_FORBIDDEN
          )
          
      if not request.data.get('password') or not request.user.check_password(request.data.get('password')):
          return Response(
                {"detail": "Please provide your password to confirm account deletion."},
                status=status.HTTP_401_UNAUTHORIZED
          )
      user.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
          
   
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
        return self.queryset.filter(participants=self.request.user).distinct()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'participants__username']
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        
    @action(detail=True, methods=['get'])
    def threaded_messages(self, request, pk=None):
        """
        Retrieves all messages for a specific conversation,
        organized into a threaded (nested) structure.
        URL: /api/conversations/{pk}/threaded_messages/
        """
        try:
            conversation = self.get_object() # Get the specific Conversation instance
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        # Optimize fetching:
        # - messages: Fetches all messages belonging to this conversation
        # - select_related('parent_message', 'sender', 'receiver'): Avoids N+1 queries for parent, sender, and receiver details.
        # - order_by('created_at'): Ensures messages are in chronological order for correct threading.
        messages_in_conversation = conversation.messages.select_related('parent_message', 'sender', 'receiver').order_by('created_at')

        # Build the threaded structure using the utility function
        threaded_data = build_threaded_messages(messages_in_conversation)

        return Response(threaded_data)

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage Messages within conversations.
    This ViewSet expects to be nested under a Conversation, e.g., /conversations/{pk}/messages/
    """
    serializer_class = MessageSerializer
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MessageFilter
    search_fields = ['content']

    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    queryset = Message.objects.all()

    @method_decorator(cache_page(60))
    def get_queryset(self): # type: ignore
        conversation_pk = self.kwargs.get('conversation_pk')
        if not conversation_pk:
            raise PermissionDenied("Conversation ID is required for message operations.")

        return (
            Message.objects
            .filter(conversation_id=conversation_pk) # Filter by the specific conversation
            .select_related('sender', 'receiver', 'parent_message') # Avoid N+1 for FKs
            .order_by('created_at')
        )

    def perform_create(self, serializer):
        conversation_pk = self.kwargs.get('conversation_pk')
        if not conversation_pk:
            raise PermissionDenied("Conversation ID is required to create a message.")

        try:
            conversation = Conversation.objects.get(pk=conversation_pk)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation not found.")

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not part of this conversation.")

        # Save the message, linking it to the current user as sender and the conversation
        request = self.request
        serializer.save(sender=request.user, conversation=conversation)

    def perform_update(self, serializer):
        if self.get_object().sender != self.request.user:
            raise PermissionDenied("You can only edit your own messages.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.sender != self.request.user:
            raise PermissionDenied("You can only delete your own messages.")
        instance.delete()
        
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(60))
    def top_messages(self, request, conversation_pk=None):
        """
        Returns only the top-level messages (messages without a parent)
        for the current conversation.
        Example URL: /api/conversations/{pk}/messages/top_messages/
        """
        # get_queryset already filters by conversation. We just add the parent_message__isnull filter.
        top_level_msgs = self.get_queryset().filter(parent_message__isnull=True) \
                                          .prefetch_related('replies') # Prefetch direct replies

        serializer = self.get_serializer(top_level_msgs, many=True)
        return Response(serializer.data)

    # Example of improving the default `retrieve` action to prefetch replies:
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object() # This uses `get_queryset` which has `select_related`
        instance = self.get_queryset().get(pk=instance.pk) # Re-query to include prefetch, if not always 
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(60))
    def unread_inbox(self, request, conversation_pk=None):
        """
        Returns unread messages for the requesting user within the specified conversation.
        URL: /api/conversations/{pk}/messages/unread_inbox/
        """
        # base_messages_in_conv = Message.objects.filter(conversation_id=conversation_pk)
        unread_messages = Message.unread.unread_for_user(request.user).select_related('sender', 'parent_message').only('id', 'sender', 'content', 'created_at', 'conversation') # type: ignore
        
        serializer = self.get_serializer(unread_messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_as_read(self, request, conversation_pk=None):
        """
        Marks specified messages as read for the requesting user within the conversation.
        Expects a list of message IDs in the request body: {"message_ids": [1, 2, 3]}
        URL: /api/conversations/{pk}/messages/mark_as_read/
        """
        message_ids = request.data.get('message_ids')

        if not isinstance(message_ids, list):
            return Response({"detail": "message_ids must be a list."}, status=status.HTTP_400_BAD_REQUEST)

        if not message_ids:
            return Response({"detail": "No message IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        updated_count = Message.objects.filter(conversation_id=conversation_pk).unread.mark_as_read(request.user, message_ids) # type: ignore

        return Response(
            {"detail": f"Successfully marked {updated_count} messages as read."},
            status=status.HTTP_200_OK
        )
        
class AdminUserListViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]