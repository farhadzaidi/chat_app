from django.db import models
from django.contrib.auth.models import User

class PrivateChat(models.Model):
	chat_name = models.CharField(max_length=100)
	chat_alias = models.CharField(max_length=100)
	group_members = models.ManyToManyField(User, related_name='members', blank=True)

	def __str__(self):
		return self.chat_alias

class Message(models.Model):
	text = models.CharField(max_length=300)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.text} by {self.author}'
