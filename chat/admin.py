from django.contrib import admin
from .models import PrivateChat, Message

admin.site.register(Message)
admin.site.register(PrivateChat)