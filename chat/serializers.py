from rest_framework import serializers
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Chat
        fields = ["id", "name", "participants", "created_at"]
        read_only_fields = ["created_at"]

class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Message
        fields = ["id", "text", "from_user", "chat", "created_at"]
        read_only_fields = ["from_user", "created_at"]
