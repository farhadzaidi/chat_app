from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	friends = models.ManyToManyField(User, related_name='friends', blank=True)

	def __str__(self):
		return f'{self.user.username}'

class FriendRequest(models.Model):
	sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	reciever = models.ForeignKey(User, related_name='reciever', on_delete=models.DO_NOTHING)

	def __str__(self):
		return f'{self.sender} to {self.reciever}'