from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with explicit CharField and validation example.
    """
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]

    def validate_role(self, value):
        """
        Example of using ValidationError.
        Ensure role is one of allowed values.
        """
        if value not in ['guest', 'host', 'admin']:
            raise serializers.ValidationError("Role must be guest, host, or admin.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message with nested sender.
    """
    sender_name = serializers.SerializerMethodField()  # dynamically computed field

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "sender_name",  # computed field
            "conversation",
            "message_body",
            "sent_at",
        ]

    def get_sender_name(self, obj):
        """
        Example of SerializerMethodField: returns full name of sender.
        """
        return f"{obj.sender.first_name} {obj.sender.last_name}"


class ConversationSerializer(serializers.ModelSerializer):
    """
    Conversation serializer with nested participants and messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "participant_count",  # dynamically computed
            "messages",
            "created_at",
        ]

    def get_participant_count(self, obj):
        """
        Returns number of participants in the conversation.
        """
        return obj.participants.count()
