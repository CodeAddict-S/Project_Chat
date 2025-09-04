from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.db import models
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

# Create chat uchun views
class ChatViewSet(viewsets.ModelViewSet):
    queryset= Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Faqat foydalanuvchi ishtirok etgan chatlarni qaytarish"""
        user = self.request.user
        return Chat.objects.filter(
            models.Q(user_1=user) | models.Q(user_2=user)
        )
    
    def create(self, request, *args, **kwargs):
            """Chat yaratishda user_1 avtomatik request.user bo'ladi"""
            data = {
                "name": request.data['name'],
                "user_1": request.user.id,
                "user_2": request.data['user']
            }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        if 'user_1' in request.data or 'user_2' in request.data:
            raise PermissionDenied()
        super().update()
        
        
    
    def perform_update(self, serializer):
        """Chat o'zgartirishdan oldin ruxsat tekshirish"""
        chat = self.get_object()
        user = self.request.user
        
        if chat.user_1_id != user.id and chat.user_2_id != user.id:
            raise PermissionDenied("Siz ushbu chatni o'zgartira olmaysiz.")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Chat o'chirishdan oldin ruxsat tekshirish"""
        user = self.request.user
        
        if instance.user_1_id != user.id and instance.user_2_id != user.id:
            raise PermissionDenied("Siz ushbu chatni o'chira olmaysiz.")
        
        instance.delete()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Faqat foydalanuvchi ishtirok etgan chatlardagi xabarlarni qaytarish"""
        user = self.request.user
        return Message.objects.filter(
            models.Q(chat__user_1=user) | models.Q(chat__user_2=user)
        )
    
    def create(self, request, *args, **kwargs):
        """Message yaratish faqat websocket orqali bo'ladi"""
        return Response(
            {"error": "Xabar yaratish faqat WebSocket orqali mumkin."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def perform_update(self, serializer):
        """Xabar o'zgartirishdan oldin ruxsat tekshirish"""
        message = self.get_object()
        user = self.request.user
        
        if message.from_user_id != user.id:
            raise PermissionDenied("Faqat yuborgan foydalanuvchi xabarni o'zgartira oladi.")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Xabar o'chirishdan oldin ruxsat tekshirish"""
        user = self.request.user
        
        if instance.from_user_id != user.id:
            raise PermissionDenied("Faqat yuborgan foydalanuvchi xabarni o'chira oladi.")
        instance.delete()
        