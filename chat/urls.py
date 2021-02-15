from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='chat-index'),
    path('chat/<slug:chat_name>/', views.public_chat, name='public-chat'),
    path('private-chat/<slug:chat_name>/', views.private_chat, name='private-chat')
]
