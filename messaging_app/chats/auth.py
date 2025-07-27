from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to interact with it or its messages.
    """
    def has_object_permission(self, request, view, obj):
        # The user must be authenticated to proceed.
        if not request.user or not request.user.is_authenticated:
            return False

        # If the object is a Conversation, check if the user is a participant.
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # If the object is a Message, check if the user is a participant of the message's conversation.
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        return False

class IsSenderOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the sender of a message to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated participant.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the sender of the message.
        return obj.sender_id == request.user
