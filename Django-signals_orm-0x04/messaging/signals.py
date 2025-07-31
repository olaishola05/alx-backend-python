from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, NotificationType, MessageHistory
import logging
from real_time import send_realtime_notification


logger = logging.getLogger(__name__)

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal handler that creates a notification when a new message is sent.
    
    Parameters:
    - sender: The Message model class
    - instance: The actual Message object that was saved
    - created: Boolean indicating if this is a new message (True) or update (False)
    """
    
    if created:
        try:
            if instance.sender == instance.receiver:
                logger.info(f"Skipping notification: User {instance.sender.username} sent message to themselves")
                return
            notification = Notification.objects.create(
                user = instance.receiver,
                notification_type = NotificationType.NEW_MESSAGE,
                title = f"New message from {instance.sender.username}",
                message=f"You have received a new message: \"{instance.content[:100]}{'...' if len(instance.content) > 100 else ''}\"",
                related_message=instance
            )
            send_realtime_notification(notification=notification)
        except Exception as e:
             logger.error(f"❌ Failed to create notification for message {instance.id}: {str(e)}")
             
@receiver(post_save, sender=Message)             
def handle_message_read_notification(sender, instance, created, **kwargs):
    """
    Optional: Create notification when sender's message is read
    """
    
    if not created and instance.is_read:
        existing_read_notification = Notification.objects.filter(
            user = instance.sender,
            notification_type = NotificationType.MESSAGE_READ,
            related_message = instance
        ).exists()
        
        if not existing_read_notification:
            try:
                notification = Notification.objects.create(
                    user = instance.sender,
                    notification_type = NotificationType.MESSAGE_READ,
                    title = f"{instance.receiver.username} read your message",
                    message=f"Your message \"{instance.content[:50]}{'...' if len(instance.content) > 50 else ''}\" has been read",
                )
                id = notification.notification_id
                logger.info(f"✅ Created read notification {id} for sender {instance.sender.username}")
                
            except Exception as e:
                logger.error(f"❌ Failed to create read notification: {str(e)}")
                
@receiver(pre_save, sender=Message)
def save_message_history(sender, instance, **kwargs):
    """
    Signal to auto save message if it is edited
    """
    
    if instance.pk:
      try:
        old_message_instance = sender.objects.get(pk=instance.pk)
        MessageHistory.objects.create(
          message = instance,
          old_content = old_message_instance.content,
          changed_by = instance.user
        )
        logger.info(f"Old version of Message {instance.pk} saved to history.")
      except Message.DoesNotExist:
        logger.error(f"Message instance does not exist")
        
@receiver(post_delete, sender=User)
def clean_up_signal(sender, instance, **kwargs):
    user_id = instance.pk
    logger.info((f"User with ID {user_id} has been deleted. Performing cleanup..."))
    
    if user_id:
        try:
            messages_sent_by_user = Message.objects.filter(sender=user_id)
            messages_received_by_user = Message.objects.filter(receiver=user_id)
            # count_sent = messages_sent_by_user.count()
            count_sent, _ =messages_sent_by_user.delete()
            count_received, _ = messages_received_by_user.delete()
            logger.info(f"Deleted {count_sent} messages sent by user {user_id}.")
            logger.info(f"Deleted {count_received} messages received by user {user_id}.")
            
            notifications_for_user = Notification.objects.filter(user=user_id)
            notifications_count = notifications_for_user.count()
            logger.info(f"Deleted {notifications_count} notifications for user {user_id}.")
            
            if instance.profile_picture:
                instance.profile_profile_picture.delete(save=False)
                logger.info(f"Deleted profile picture for user {user_id}")
        except User.DoesNotExist as e:
            logger.error(f"User does not exist {str(e)}")
        except Exception as e:
            logger.error(f" fatal error {str(e)}")
            
    logger.info(f"Explicit cleanup for user {user_id} complete.")