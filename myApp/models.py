from django.db import models
import uuid

class User(models.Model) :
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=20)
    user_password = models.CharField(max_length=130)
    user_email = models.CharField(max_length=30)
    user_balance = models.BigIntegerField(default=10000)
    def __str__(self):
        return self.user_name
    


class Flag(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_flags = models.JSONField(default={"sms": False, "whatsapp": False, "url_shortner": False})
    def __str__(self):
        return ""
