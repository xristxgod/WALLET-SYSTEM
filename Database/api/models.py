from django.db import models

class UserModel(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"ID: {self.id} | {self.username}"