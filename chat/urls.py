from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='chat-index'),
    path('chat/<slug:room_name>/', views.public_room, name='chat-room'),
    path('private-chat/<slug:room_name>/', views.private_room, name='private-chat-room')
]
