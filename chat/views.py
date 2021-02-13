from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import FriendRequest
from django.contrib import messages
from django.http import JsonResponse
from users.models import Profile

def index(request):

	# AJAX requests
	if request.is_ajax():

		# AJAX POST requests
		if request.method == 'POST':

			if 'friendName' in request.POST:

				sender = request.user
				reciever = User.objects.get(username=request.POST['friendName'])

				friend_request = FriendRequest(sender=sender, reciever=reciever)
				friend_request.save()

				messages.success(request, f'Friend request sent to {reciever}')

				return JsonResponse({}, status=200)


			if 'acceptFriendPK' in request.POST:

				sender = User.objects.get(pk=request.POST['acceptFriendPK'])
				reciever = request.user

				sender.profile.friends.add(reciever)
				reciever.profile.friends.add(sender)

				friend_request = FriendRequest.objects.get(sender=sender, reciever=reciever)
				friend_request.delete()

				messages.success(request, f'You and {sender} are now friends!')

				return JsonResponse({}, status=200)

			if 'declineFriendPK' in request.POST:

				sender = User.objects.get(pk=request.POST['declineFriendPK'])
				reciever = request.user

				friend_request = FriendRequest.objects.get(sender=sender, reciever=reciever)
				friend_request.delete()

				return JsonResponse({}, status=200)


		# AJAX GET requests
		data = {}

		if 'getData' in request.GET: 
			
			# get usernames 
			usernames = [user.username for user in User.objects.all()]
			data['usernames'] = usernames

			# get user's friends list
			friends = request.user.profile.friends.all()
			friends_list = [friend.username for friend in friends]
			data['friends_list'] = friends_list

			# get user's sent friend requests
			friend_requests = FriendRequest.objects.filter(sender=request.user)
			pending_friend_requests = [friend_request.reciever.username for friend_request in friend_requests]
			print(pending_friend_requests)
			data['pending_friend_requests'] = pending_friend_requests

			# get primary keys of users who sent friend requests to the current user
			friend_requests = FriendRequest.objects.filter(reciever=request.user)
			friend_request_pks = []
			for friend_request in friend_requests:
				friend_request_pks.append(friend_request.sender.pk)

			data['friend_request_pks'] = friend_request_pks

		return JsonResponse(data, status=200)



	# POST requests
	if request.method == 'POST':

		# create private room 
		if 'private-room-name' in request.POST:

			return render(request, 'chat/index.html')

		# enter public room
		if 'room-name' in request.POST:
			room_name = request.POST['room-name']
			username = request.POST['username']

			request.session['username'] = username

			return redirect(reverse('chat-room', kwargs={'room_name': room_name}))


	# GET requests
	context = {
		'title': 'Home',
	}

	if request.user.is_authenticated:
		context['authenticated'] = 'yes'
	else:
		context['authentictaed'] = 'no'

	if request.user.is_authenticated:
		friend_requests = FriendRequest.objects.filter(reciever=request.user)
		context['friend_requests'] = friend_requests

	return render(request, 'chat/index.html', context)



def room(request, **kwargs):
	context = {
		'room_name': kwargs['room_name'],
		'username': request.session['username'],
	}

	return render(request, 'chat/room.html', context)