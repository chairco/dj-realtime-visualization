from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    """
    save user submitted
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_name = models.TextField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


