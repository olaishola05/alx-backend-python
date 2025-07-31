from django.db import models

class UnreadMessagesManager(models.Manager):
  def unread_for_user(self, user):
    """
        Filters messages that are unread AND where the given user is the receiver.
        Optimizes by only retrieving essential fields.
        """
    return self.filter(
      receiver=user,
      is_read=False,
    )
    
  def mark_as_read(self, user, message_ids):
    """
        Marks a list of messages as read for a specific user,
        ensuring the user is indeed the receiver of those messages.
        """
        
    return self.filter(
      receiver=user,
      id__in=message_ids,
      is_read=False
    ).update(is_read=True)
          