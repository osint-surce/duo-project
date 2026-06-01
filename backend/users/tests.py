from django.test import TestCase
from django.contrib.auth.models import User

class UserTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username="test",
            password="123456"
        )

        self.assertEqual(
            user.username,
            "test"
        )
