from django.contrib import admin
from .models import PrivateChat, Message, PrivateChatInvitation

admin.site.register(Message)
admin.site.register(PrivateChat)
admin.site.register(PrivateChatInvitation)