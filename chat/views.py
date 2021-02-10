from django.shortcuts import render, redirect
from django.urls import reverse

def index(request):

	if request.method == 'POST':
		room_name = request.POST['room-name']
		guest_name = request.POST['guest-name']

		request.session['guest_name'] = guest_name

		return redirect(reverse('chat-room', kwargs={'room_name': room_name}))

	return render(request, 'chat/index.html')

def room(request, **kwargs):
	context = {
		'room_name': kwargs['room_name'],
		'guest_name': request.session['guest_name'],
	}

	return render(request, 'chat/room.html', context)