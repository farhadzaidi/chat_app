from django.db import models
from django.contrib.auth.models import User

class PrivateChat(models.Model):
	name = models.CharField(max_length=100)
	alias = models.CharField(max_length=100)
	members = models.ManyToManyField(User, related_name='members', blank=True)

	def __str__(self):
		return self.alias

class PrivateChatInvitation(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	reciever = models.ForeignKey(User, related_name='chat_invite_reciever', on_delete=models.CASCADE)
	chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.sender} to {self.reciever} for {self.chat}'

class Message(models.Model):
	text = models.CharField(max_length=300)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.text} by {self.author}'

