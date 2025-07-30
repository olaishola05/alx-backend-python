
from django.core.mail import send_mail
from django.conf import settings
import logging

 # WebSocket notification (Django Channels)
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


logger = logging.getLogger(__name__)


def send_realtime_notification(notification):
    """
    Handle real-time notification delivery
    
    This is where you'd integrate with:
    - WebSockets (Django Channels)
    - Push notifications (Firebase, APNs)
    - Email notifications
    - SMS notifications
    - Browser notifications
    
    Keeping this separate makes the system more modular
    """
    
    try:
        logger.info(f"🔔 Real-time notification: {notification.title} for {notification.user.username}")
        
        # Example integrations (uncomment and implement as needed):
        # 
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{notification.user.id}",
            {
                "type": "notification_message",
                "notification": {
                    "id": notification.id,
                    "title": notification.title,
                    "message": notification.message,
                    "created_at": notification.created_at.isoformat(),
                }
            }
        )
        
        if notification.user.email:
            send_mail(
                subject=notification.title,
                message=notification.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.user.email],
                fail_silently=True,
            )
        
        # # Push notification (using a service like Firebase)
        # send_push_notification(
        #     user_id=notification.user.id,
        #     title=notification.title,
        #     body=notification.message
        # )
        
    except Exception as e:
        logger.error(f"❌ Failed to send real-time notification: {str(e)}")

