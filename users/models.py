from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=100, unique=True,null=False)
    password = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=15, null=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email, self.username
    class Meta:
        db_table = 'users'