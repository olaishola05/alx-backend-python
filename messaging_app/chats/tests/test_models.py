from django.test import TestCase
from models import User, Conversation, Message
from django.db import IntegrityError
from django.conf import settings
import uuid
from datetime import datetime

class UserModelTest(TestCase):
    """
      Test the User model.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('testpass'))
        
    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')
        
    def test_user_email_unique(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username='anotheruser',
                email='testuser@example.com',
                password='testpass'
            )
            self.assertTrue(User.objects.filter(username='anotheruser').exists())
            self.assertFalse(User.objects.filter(email='testuser@example.com').exists())
            
    def test_user_phone_number_blank(self):
        user = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testpass'
        )
        self.assertEqual(user.phone_number, '')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        
    def test_user_profile_picture(self):
        user = User.objects.create_user(
            username='testuser3',
            email='testuser3@example.com',
            password='testpass'
        )
        self.assertEqual(user.profile_picture, '')
        self.assertEqual(user.profile_picture, settings.DEFAULT_PROFILE_PICTURE)
        
    def test_user_is_online_default(self):
        user = User.objects.create_user(
            username='testuser4',
            email='testuser4@example.com',
            password='testpass'
        )
        self.assertFalse(user.is_online)

    def test_user_is_online(self):
        user = User.objects.create_user(
            username='testuser5',
            email='testuser5@example.com',
            password='testpass'
        )
        user.is_online = True
        user.save()
        self.assertTrue(user.is_online)
        self.assertEqual(user._meta.verbose_name_plural, 'Messages')
        self.assertEqual(user._meta.verbose_name, 'Message')
        self.assertEqual(user._meta.model_name, 'user')
        self.assertEqual(user._meta.app_label, 'chats')


    def test_user_id_is_uuid(self):
        user = User.objects.create_user(
            username='testuser6',
            email='testuser6@example.com',
            password='testpass'
          )
        self.assertIsInstance(user.user_id, uuid.UUID)

    def test_user_update_email(self):
        user = User.objects.create_user(
            username='testuser7',
            email='testuser7@example.com',
            password='testpass'
        )
        user.email = 'newemail@example.com'
        user.save()
        
        user.password = 'newpassword'
        user.save()

        self.assertTrue(user.check_password('newpassword'))
        self.assertEqual(user.email, 'newemail@example.com')

class ConversationModelTest(TestCase):
    """
      Test the Conversation model.
    """
    def setUp(self):
        self.conversation = Conversation.objects.create(
            participants=[User.objects.create_user(
                username='testuser',
                email='testuser@example.com',
                password='testpass'
            )]
        )

    def test_conversation_creation(self):
        self.assertEqual(self.conversation.participants.count(), 1)

    def test_conversation_str(self):
        self.assertEqual(str(self.conversation), 'Test Conversation')
        
    def test_conversation_participants(self):
        self.assertEqual(self.conversation.participants.count(), 1)
        self.assertEqual(self.conversation.participants.first().username, 'testuser')
    
    def test_conversation_created_at(self):
        self.assertIsInstance(self.conversation.created_at, datetime)
        
    def test_conversation_id_is_uuid(self):
        self.assertIsInstance(self.conversation.conversation_id, uuid.UUID)
        
    def test_conversation_ordering(self):
        conversation2 = Conversation.objects.create(
            participants=[User.objects.create_user(
                username='testuser2',
                email='testuser2@example.com',
                password='testpass'
            )]
        )
        self.assertLess(self.conversation.created_at, conversation2.created_at)


    def test_multiple_participants(self):
        user2 = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testpass'
        )
        user3 = User.objects.create_user(
            username='testuser3',
            email='testuser3@example.com',
            password='testpass'
        )
        self.conversation.participants.add(user2, user3)
        self.assertEqual(self.conversation.participants.count(), 3)
        
        
    def test_conversation_verbose_name_plural(self):
        self.assertEqual(self.conversation._meta.verbose_name_plural, 'Conversations')

    def test_participants_related_name(self):
        self.assertEqual(self.conversation.participants.get('related_name'), 'conversations')
        
        
class MessageModelTest(TestCase):
    """
      Test the Message model.
    """
    def setUp(self):
        self.message = Message.objects.create(
            sender=User.objects.create_user(
                username='testuser',
                email='testuser@example.com',
                password='testpass'
            ),
            message_body='Hello, world!',
            conversation=Conversation.objects.create(
                participants=[User.objects.create_user(
                    username='testuser2',
                    email='testuser2@example.com',
                    password='testpass'
                )]
            )
        )

    def test_message_creation(self):
        self.assertEqual(self.message.message_body, 'Hello, world!')
        self.assertIsInstance(self.message.created_at, datetime)

    def test_message_sender(self):
        self.assertEqual(self.message.sender.username, 'testuser')

    def test_message_conversation(self):
        self.assertEqual(self.message.conversation.participants.count(), 2)

    def test_message_str(self):
        self.assertEqual(str(self.message), 'Hello, world!')

    def test_message_id_is_uuid(self):
        self.assertIsInstance(self.message.message_id, uuid.UUID)

    def test_message_ordering(self):
        message2 = Message.objects.create(
            sender=User.objects.create_user(
                username='testuser3',
                email='testuser3@example.com',
                password='testpass'
            ),
            content='Hello, again!',
            conversation=self.message.conversation
        )
        self.assertLess(self.message.created_at, message2.created_at)