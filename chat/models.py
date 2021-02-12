from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.CharField(max_length=200)
	notification_type = models.CharField(max_length=20)
	read = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.notification_type} for {self.user}'