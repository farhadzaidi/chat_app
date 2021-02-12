from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Notification

def index(request):


	if request.method == 'POST':

		if 'private-room-name' in request.POST:

			return render(request, 'chat/index.html')

		if 'friend-name' in request.POST:

			friend_request_sender = request.user

			friend_request_reciever = User.objects.get(username=request.POST['friend-name'])
			notification_text = f'{friend_request_sender} has sent you a friend request.'
			notification_type = 'friend-request'

			new_notification = Notification(user=friend_request_reciever, text=notification_text, notification_type='friend-request')
			new_notification.save()

			return render(request, 'chat/index.html')


		room_name = request.POST['room-name']
		username = request.POST['username']

		request.session['username'] = username

		return redirect(reverse('chat-room', kwargs={'room_name': room_name}))


	context = {'title': 'Home'}

	if request.user.is_authenticated:
		notifications = Notification.objects.filter(user=request.user)
		context['notifications'] = notifications

	return render(request, 'chat/index.html', context)

def room(request, **kwargs):
	context = {
		'room_name': kwargs['room_name'],
		'username': request.session['username'],
	}

	return render(request, 'chat/room.html', context)