from django.urls import path
from chat.views import ChatViewSet

urlpatterns = [
    path('new_chat/', ChatViewSet.as_view(), name='new_chat'),
]
