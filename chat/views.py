from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

User = get_user_model()


class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Faqat foydalanuvchi ishtirok etgan chatlarni qaytarish"""
        user = self.request.user
        return Chat.objects.filter(participants=user)

    def create(self, request, *args, **kwargs):
        chat_name = request.data.get("name")
        # ❌ Eski kod: username = request.data.get("username")
        # ✅ Yangi kod: frontenddan keladigan to'g'ri field nomini ishlatish
        recipient_username = request.data.get("recipient_username")

        # recipient_username orqali foydalanuvchini topish
        try:
            participant = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            return Response(
                {"error": "Bunday foydalanuvchi topilmadi."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # chat yaratish va ishtirokchilarni qo'shish
        chat = Chat.objects.create(name=chat_name)
        chat.participants.add(request.user, participant)

        serializer = self.get_serializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        """Chatni o'zgartirishdan oldin ruxsat tekshirish"""
        chat = self.get_object()
        user = self.request.user
        if not chat.participants.filter(id=user.id).exists():
            raise PermissionDenied("Siz ushbu chatni o'zgartira olmaysiz.")
        serializer.save()

    def perform_destroy(self, instance):
        """Chatni o'chirishdan oldin ruxsat tekshirish"""
        user = self.request.user
        if not instance.participants.filter(id=user.id).exists():
            raise PermissionDenied("Siz ushbu chatni o'chira olmaysiz.")
        instance.delete()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Faqat foydalanuvchi ishtirok etgan chatlardagi xabarlarni qaytarish"""
        user = self.request.user
        return Message.objects.filter(chat__participants=user)

    def create(self, request, *args, **kwargs):
        """Message yaratish faqat WebSocket orqali bo'ladi"""
        return Response(
            {"error": "Xabar yaratish faqat WebSocket orqali mumkin."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def perform_update(self, serializer):
        """Xabarni o'zgartirishdan oldin ruxsat tekshirish"""
        message = self.get_object()
        user = self.request.user
        if message.from_user_id != user.id:
            raise PermissionDenied("Faqat yuborgan foydalanuvchi xabarni o'zgartira oladi.")
        serializer.save()

    def perform_destroy(self, instance):
        """Xabarni o'chirishdan oldin ruxsat tekshirish"""
        user = self.request.user
        if instance.from_user_id != user.id:
            raise PermissionDenied("Faqat yuborgan foydalanuvchi xabarni o'chira oladi.")
        instance.delete()