from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import uuid

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('guest', 'Guest'),
        ('host', 'Host')
    ]

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False, db_index=True)
    password_hash = models.CharField(max_length=100, blank=False, null=False)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.username

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_user_email'),
        ]
        indexes = [
            models.Index(fields=['email'], name='user_email_idx'),
        ]

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField('User', related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_participants_names(self):
        """Return comma-separated participant names."""
        return ", ".join([p.get_full_name() for p in self.participants.all()])

    def __str__(self):
        return f"Conversation {self.conversation_id}"

    class Meta:
        indexes = [
            models.Index(fields=['created_at'], name='conversation_created_at_idx'),
        ]


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', null=False)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', null=False)
    recipient_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=False)
    message_body = models.TextField(blank=False, null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender_id.username} to {self.recipient_id.username} at {self.sent_at}"

    class Meta:
        ordering = ['-sent_at']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(sender_id=models.F('recipient_id')),
                name='message_sender_not_recipient'
            ),
        ]
        indexes = [
            models.Index(fields=['sender_id'], name='message_sender_idx'),
            models.Index(fields=['recipient_id'], name='message_recipient_idx'),
            models.Index(fields=['conversation'], name='message_conversation_idx'),
            models.Index(fields=['sent_at'], name='message_sent_at_idx'),
        ]

