from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='chat-index'),
    path('chat/<slug:room_name>/', views.room, name='chat-room')
]
