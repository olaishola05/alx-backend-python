from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import datetime

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.URLField(max_length=200, blank=False, null=True)
    is_online = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversation')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Conversations'
        
        
class Message(models.Model):
  message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages',
        help_text="User who sent the message")
  receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages',
        help_text="User who will receive the message")
  content = models.TextField(max_length=1000, help_text="The actual message content")
  timestamp = models.DateTimeField(default=datetime.now, db_index=True,help_text="When the message was created")
  is_read = models.BooleanField(default=False)
  edited = models.BooleanField(default=False)
  
  def __str__(self) -> str:
      return f"Message from {self.sender.username} to {self.receiver.username}: {self.content[:50]}..."
    
  class Meta:
    ordering = ['-timestamp']
    verbose_name_plural = 'Messages'
    unique_togther = ('sender', 'content')
    indexes = [
            models.Index(fields=['receiver', '-timestamp']),
            models.Index(fields=['sender', '-timestamp']),
        ]
    
  def mark_as_read(self):
      """Helper method to mark message as read"""
      if not self.is_read:
        self.is_read = True
        self.save(update_fields=['is_read'])
        
        
        
class NotificationType(models.TextChoices):
    """
    Enum for different notification types
    """
    
    NEW_MESSAGE = 'new_message', 'New Message'
    MESSAGE_READ = 'message_read', 'Message Read'
    FRIEND_REQUEST = 'friend_request', 'Friend Request'
    SYSTEM_ALERT = 'system_alert', 'System Alert'
    
    
class Notification(models.Model):
  notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',
        help_text="User who will receive this notification")
  notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.NEW_MESSAGE,
        help_text="Type of notification"
    )
  title = models.CharField(max_length=100, help_text="Notification title/subject")
  message = models.TextField(max_length=500, help_text="Notification body/content")
  related_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
  is_read = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True, db_index=True)
  
  
  def __str__(self):
    status = "📬" if not self.is_read else "📭"
    return f"{status} {self.title} for {self.user.username}"
  
  class Meta:
    ordering = ['-created_at']
    verbose_name_plural = 'Notifcations'
    unique_together = ['user', 'messages']
    indexes = [
            models.Index(fields=['user', 'is_read', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
    
  def mark_as_read(self):
    """Helper method to mark message as read"""
    if not self.is_read:
      self.is_read = True
      self.save(update_fields=['is_read'])
      
      
class MessageHistory(models.Model):
    history = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='old_message')
    old_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    
    def __str__(self):
        return f"Saved {self.message.content} for {self.message.sender} in history table"
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Notifcations'
        unique_together = ['user', 'messages']
        indexes = [
          models.Index(fields=['user', '-created_at']),
        ]