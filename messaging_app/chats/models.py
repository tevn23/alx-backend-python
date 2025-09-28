# chats/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

# ------------------------
# Custom User model
# ------------------------
class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    Attributes:
        user_id (UUIDField): Primary key, auto-generated UUID.
        phone_number (str): Optional phone number of the user.
        role (str): Role of the user. Choices are 'guest', 'host', 'admin'.
        groups (ManyToMany): Groups this user belongs to (custom related_name to avoid clashes).
        user_permissions (ManyToMany): Specific permissions for this user (custom related_name).
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        """String representation of the User."""
        return f"{self.username} ({self.email})"

# ------------------------
# Conversation model
# ------------------------
class Conversation(models.Model):
    """
    Conversation model representing a chat room between users.

    Attributes:
        conversation_id (UUIDField): Primary key, auto-generated UUID.
        participants (ManyToMany): Users participating in this conversation.
        created_at (DateTimeField): Timestamp when the conversation was created.
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the Conversation."""
        return f"Conversation {self.conversation_id}"

# ------------------------
# Message model
# ------------------------
class Message(models.Model):
    """
    Message model representing a message sent by a user in a conversation.

    Attributes:
        message_id (UUIDField): Primary key, auto-generated UUID.
        sender (ForeignKey): User who sent the message.
        conversation (ForeignKey): Conversation this message belongs to.
        message_body (TextField): The content of the message.
        sent_at (DateTimeField): Timestamp when the message was sent.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the Message."""
        return f"Message {self.message_id} from {self.sender.username}"
