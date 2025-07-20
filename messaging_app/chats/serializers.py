from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']

class UserSummarySerializer(serializers.ModelSerializer):
    """Lightweight User serializer for nested relationships to avoid circular references"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'first_name',
            'last_name',
            'full_name'
        ]
        read_only_fields = ['user_id']

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with nested user information"""
    sender = UserSummarySerializer(source='sender_id', read_only=True)
    recipient = UserSummarySerializer(source='recipient_id', read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    recipient_id = serializers.UUIDField(write_only=True)
    sender_name = serializers.CharField(source='sender_id.get_full_name', read_only=True)
    recipient_name = serializers.CharField(source='recipient_id.get_full_name', read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'recipient',
            'sender_id',
            'recipient_id',
            'sender_name',
            'recipient_name',
            'conversation',
            'message_body',
            'sent_at',
        ]
        read_only_fields = ['message_id', 'sent_at']

    def validate(self, data):
        """Ensure sender and recipient are different users"""
        if data.get('sender_id') == data.get('recipient_id'):
            raise serializers.ValidationError("Sender and recipient cannot be the same user.")
        return data

class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested participants and messages"""
    participants = UserSummarySerializer(many=True, read_only=True)
    participants_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    participants_names = serializers.CharField(source='get_participants_names', read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participants_ids',
            'participants_names',
            'messages',
            'message_count',
            'last_message',
            'created_at',
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def get_message_count(self, obj):
        """Get total number of messages in the conversation"""
        return obj.messages.count()

    def get_last_message(self, obj):
        """Get the most recent message in the conversation"""
        last_message = obj.messages.first()
        if last_message:
            return {
                'message_id': last_message.message_id,
                'message_body': last_message.message_body,
                'sender': last_message.sender_id.username,
                'sent_at': last_message.sent_at
            }
        return None

    def create(self, validated_data):
        """Create conversation with participants"""
        participants_ids = validated_data.pop('participants_ids', [])
        conversation = Conversation.objects.create(**validated_data)

        if participants_ids:
            users = User.objects.filter(user_id__in=participants_ids)
            conversation.participants.set(users)

        return conversation

    def update(self, instance, validated_data):
        """Update conversation and participants"""
        participants_ids = validated_data.pop('participants_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if participants_ids is not None:
            users = User.objects.filter(user_id__in=participants_ids)
            instance.participants.set(users)

        return instance

class ConversationListSerializer(serializers.ModelSerializer):
    """Lightweight Conversation serializer for list views"""
    participants = UserSummarySerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    participants_preview = serializers.CharField(read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participants_preview',
            'message_count',
            'last_message',
            'created_at',
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_last_message(self, obj):
        last_message = obj.messages.first()
        if last_message:
            return {
                'message_body': last_message.message_body[:50] + '...' if len(last_message.message_body) > 50 else last_message.message_body,
                'sender': last_message.sender_id.username,
                'sent_at': last_message.sent_at
            }
        return None
