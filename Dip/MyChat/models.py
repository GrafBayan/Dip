from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_chats')
    users = models.ManyToManyField(User, related_name='chats')
    invited_users = models.ManyToManyField(User, related_name='invited_chats', blank=True)

    def __str__(self):
        return self.name


class ChatInvite(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='invites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invites')
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')

    class Meta:
        unique_together = ('chat', 'user')

class ChatJoinRequest(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='join_requests')
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')

    class Meta:
        unique_together = ('chat', 'user')

    def __str__(self):
        return f"{self.user} requests to join {self.chat}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.text}'