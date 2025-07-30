from django.apps import AppConfig
from .signals import logger

class MessagingConfig(AppConfig):
    """
    App configuration that ensures signals are properly connected
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'
    
    def ready(self):
      """
      Called when Django starts up - perfect place to import signals
      """
      try:
        import messaging.signals
        
        logger.info("✅ Message notification signals registered successfully")
      except ImportError as e:
        logger.error(f"❌ Failed to import signals: {str(e)}")
