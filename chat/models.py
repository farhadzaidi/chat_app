from django.db import models
from django.contrib.auth.models import User

class PrivateChat(models.Model):
	chat_name = models.CharField(max_length=100)
	chat_alias = models.CharField(max_length=100)
	admins = models.ManyToManyField(User, blank=True)
	group_members = models.ManyToManyField(User, related_name='members', blank=True)

	def __str__(self):
		return self.chat_alias
