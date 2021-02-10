from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	friends = models.ManyToManyField(User, related_name='friends', blank=True)


	def __str__(self):
		return f'{self.user.username}'