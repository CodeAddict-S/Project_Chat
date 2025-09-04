from django.urls import include, path
from chat.views import ChatViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('chat', ChatViewSet)


urlpatterns = [
    path("", include(router.urls)), 
]
