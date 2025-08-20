from django.test import TestCase
from messaging_app.chats import serializers
from serializers import User, WelcomeSerializer, CustomTokenObtainPairSerializer

class WelcomeSerializerTest(TestCase):
    def setUp(self):
        self.serializer = WelcomeSerializer()

    def test_welcome_serializer(self):
        data = {'message': 'Welcome to the chat!'}
        self.assertEqual(self.serializer.validate(data), data)

class CustomTokenObtainPairSerializerTest(TestCase):
    def setUp(self):
        self.serializer = CustomTokenObtainPairSerializer()

    def test_custom_token_obtain_pair_serializer(self):
        data = {'username': 'testuser', 'password': 'testpass'}
        self.assertEqual(self.serializer.validate(data), data)

    def test_validate(self):
        data = {'username': 'testuser', 'password': 'testpass'}
        self.assertEqual(self.serializer.validate(data), data)