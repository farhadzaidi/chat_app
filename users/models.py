from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	friends = models.ManyToManyField(User, related_name='friends', blank=True)
	unverified_email = models.CharField(max_length=100, blank=True)
	profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pictures')

	def save(self):
		super().save()

		profile_picture = Image.open(self.profile_picture.path)

		if profile_picture.height > 300 or profile_picture.width > 300:
			size = (300, 300)
			profile_picture.thumbnail(size)
			profile_picture.save(self.profile_picture.path)


	def __str__(self):
		return f'{self.user.username}'


class FriendRequest(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	reciever = models.ForeignKey(User, related_name='reciever', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.sender} to {self.reciever}'