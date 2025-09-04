from django.urls import include, path
from chat.views import ChatViewSet, MessageViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('chat', ChatViewSet)
router.register('messages', MessageViewSet)

urlpatterns = [
    path("", include(router.urls)), 
]
