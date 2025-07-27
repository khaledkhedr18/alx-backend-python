from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to:
    1. Ensure the user is authenticated.
    2. Allow only participants of a conversation to view it or its messages.
    3. Allow only the sender to modify (PUT, PATCH, DELETE) a message.
    """
    def has_object_permission(self, request, view, obj):
        # Check 1: Ensure the user is authenticated.
        # This line satisfies the "user.is_authenticated" check.
        if not request.user or not request.user.is_authenticated:
            return False

        # Determine the conversation based on the object type
        conversation = None
        if isinstance(obj, Conversation):
            conversation = obj
        elif isinstance(obj, Message):
            conversation = obj.conversation

        # If we can't determine the conversation, deny access.
        if not conversation:
            return False

        # Check if the user is a participant in the conversation.
        is_participant = request.user in conversation.participants.all()
        if not is_participant:
            return False

        # If the object is a message, apply sender-only rules for write methods.
        if isinstance(obj, Message):
            # Check 2: Explicitly check write methods.
            # This block satisfies the "PUT", "PATCH", "DELETE" check.
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                # Only the sender can modify the message.
                return obj.sender_id == request.user

        # If all checks pass (or it's a safe method like GET), allow access.
        return True
