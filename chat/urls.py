from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_view, name='chat-index'),
    path('chat/<slug:chat_name>/', views.public_chat_view, name='public-chat'),
    path('private-chat/<slug:chat_name>/', views.private_chat_view, name='private-chat'),
]
