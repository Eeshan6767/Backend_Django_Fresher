from django.test import TestCase
from .models import User, Flag

class UserModelTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            user_name="testuser",
            user_password="test",
            user_email="testpassword@gmail.com",
            user_balance=10000
        )

    def test_user_str_representation(self):
        user = User.objects.get(user_name="testuser")
        self.assertEqual(str(user), "testuser")

    def test_user_balance_default(self):
        user = User.objects.get(user_name="testuser")
        self.assertEqual(user.user_balance, 10000)

    def test_user_correct_mail_id(self):
        user = User.objects.get(user_name="testuser")
        index = user.user_email.index('@')
        self.assertGreater(index,1, f'{index} is greater than 1')
    
    def test_user_created(self):
        user = User.objects.get(user_name="testuser")
        self.assertEqual(user.user_name, 'testuser')

class FlagModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            user_name="testuser",
            user_password="testpassword",
            user_email="test@example.com",
            user_balance=10000
        )
        Flag.objects.create(user_id=user)

    def test_flag_str_representation(self):
        flag = Flag.objects.get(user_id__user_name="testuser")
        self.assertEqual(str(flag), "")

    def test_default_user_flags(self):
        flag = Flag.objects.get(user_id__user_name="testuser")
        self.assertEqual(flag.user_flags, {})

    def test_user_flags_update(self):
        flag = Flag.objects.get(user_id__user_name="testuser")
        flag.user_flags = {"sms": True, "whatsapp": False, "url_shortner": True}
        flag.save()
        updated_flag = Flag.objects.get(user_id__user_name="testuser")
        self.assertEqual(updated_flag.user_flags, {"sms": True, "whatsapp": False, "url_shortner": True})

    def test_flag_created(self):
        flag = Flag.objects.get(user_id__user_name="testuser")
        self.assertEqual(flag.user_id.user_name, 'testuser')
