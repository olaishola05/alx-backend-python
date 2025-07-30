from django.db.models import Q
from .models import Message, Notification
from .signals import logger

class MessageManager:
    """
    Utility class for common message operations
    
    Why create this:
    - Encapsulates business logic
    - Provides consistent interface
    - Easy to test and maintain
    - Can be reused across views
    """
    
    @staticmethod
    def send_message(sender, receiver, content):
        """
        Send a message between users
        
        Returns:
            Message: The created message object
            
        Raises:
            ValueError: If sender == receiver or content is empty
        """
        
        if sender == receiver:
            raise ValueError("Cannot send message to yourself")
        
        if not content.strip():
            raise ValueError("Message content cannot be empty")
        
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content.strip()
        )
        
        logger.info(f"📨 Message sent from {sender.username} to {receiver.username}")
        return message
    
    @staticmethod
    def get_conversation(user1, user2):
        """
        Get all messages between two users
        
        Returns:
            QuerySet: Messages between the two users, ordered by timestamp
        """
        
        return Message.objects.filter(
            Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1)
        ).order_by('timestamp')
    
    @staticmethod
    def get_user_inbox(user):
        """
        Get all messages received by a user
        
        Returns:
            QuerySet: Messages received by the user, newest first
        """
        
        return Message.objects.filter(receiver=user).select_related('sender')
    
    @staticmethod
    def get_unread_messages(user):
        """
        Get unread messages for a user
        
        Returns:
            QuerySet: Unread messages for the user
        """
        
        return Message.objects.filter(receiver=user, is_read=False).select_related('sender')
    
    @staticmethod
    def mark_conversation_as_read(user, other_user):
        """
        Mark all messages from other_user to user as read
        
        Returns:
            int: Number of messages marked as read
        """
        
        return Message.objects.filter(
            sender=other_user,
            receiver=user,
            is_read=False
        ).update(is_read=True)


class NotificationManager:
    """
    Utility class for notification operations
    """
    
    @staticmethod
    def get_user_notifications(user, limit=20):
        """
        Get recent notifications for a user
        
        Returns:
            QuerySet: Recent notifications for the user
        """
        
        return Notification.objects.filter(user=user)[:limit]
    
    @staticmethod
    def get_unread_notifications(user):
        """
        Get unread notifications for a user
        
        Returns:
            QuerySet: Unread notifications for the user
        """
        
        return Notification.objects.filter(user=user, is_read=False)
    
    @staticmethod
    def mark_all_as_read(user):
        """
        Mark all notifications as read for a user
        
        Returns:
            int: Number of notifications marked as read
        """
        
        return Notification.objects.filter(user=user, is_read=False).update(is_read=True)
    
    @staticmethod
    def get_notification_count(user):
        """
        Get count of unread notifications
        
        Returns:
            int: Number of unread notifications
        """
        
        return Notification.objects.filter(user=user, is_read=False).count()

