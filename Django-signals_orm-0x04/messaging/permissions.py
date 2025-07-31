from rest_framework import permissions
from .models import Conversation


class IsOwnerOrParticipantOrReadOnly(permissions.BasePermission):
    """
    Allow owner or participant to modify, others can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        obj = view.get_object()
        return bool(
            (hasattr(obj, 'owner') and request.user == obj.owner)
            or
            (hasattr(obj, 'participants') and request.user in obj.participants.all())
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
                hasattr(obj, 'owner') and request.user == obj.owner
        ) or (
                hasattr(obj, 'participants') and request.user in obj.participants.all()
        )


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access for unauthenticated users, write access for authenticated users.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        if hasattr(obj, 'sender'):
            return request.user == obj.sender
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow only admins to modify, others can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsMessageSender(permissions.BasePermission):
    """
    Allow only the sender of a message to access it.
    """
    def has_permission(self, request, view):
        message = view.get_object()
        return request.user == message.sender

    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender


class IsConversationParticipant(permissions.BasePermission):
    """
    Allow only participants of a conversation to access it.
    """
    def has_permission(self, request, view):
        conversation = view.get_object()
        return request.user in conversation.participants.all()

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if view.action in ['list', 'create', 'top_messages', 'unread_inbox', 'mark_as_read']: # Add new actions here
            conversation_pk = view.kwargs.get('conversation_pk')
            if not conversation_pk:
                return False 
            try:
                conversation = Conversation.objects.get(pk=conversation_pk)
                return request.user in conversation.participants.all()
            except Conversation.DoesNotExist:
                return False
        
        return True

    def has_object_permission(self, request, view, obj):
        return request.user in obj.conversation.participants.all()

# class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants of a conversation to access it.
    Only allow PUT, PATCH, DELETE if user is a participant and authenticated.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            conversation = view.get_object()
            return request.user in conversation.participants.all()

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user in obj.participants.all()
        return True