from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile, FriendRequest
from django.contrib import messages
from django.http import JsonResponse
from .models import Message, PrivateChat
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from pytz import timezone
from django.core.exceptions import PermissionDenied

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

			if 'chatName' in request.POST:

				chat_name = get_random_string(length=16)
				chat_alias = request.POST['chatName']
				admin = request.user
				group_members = [User.objects.get(username=friend) for friend in request.POST.getlist('inviteFriends[]')]

				new_private_chat = PrivateChat(chat_name=chat_name, chat_alias=chat_alias)
				new_private_chat.save()

				new_private_chat.admins.add(admin)

				for group_member in group_members:
					new_private_chat.group_members.add(group_member)

				new_private_chat.group_members.add(request.user)

				new_private_chat.save()

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
			data['pending_friend_requests'] = pending_friend_requests

			# get primary keys of users who sent friend requests to the current user
			friend_requests = FriendRequest.objects.filter(reciever=request.user)
			friend_request_pks = [friend_req.sender.pk for friend_req in friend_requests]
			data['friend_request_pks'] = friend_request_pks

			# get names of user's private chats
			private_chats = PrivateChat.objects.filter(group_members=request.user)
			private_chat_names = [chat.chat_alias for chat in private_chats]
			data['private_chat_names'] = private_chat_names

		return JsonResponse(data, status=200)



	# POST requests
	if request.method == 'POST':

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

		friend_requests = FriendRequest.objects.filter(reciever=request.user)
		context['friend_requests'] = friend_requests

		private_chats = PrivateChat.objects.filter(group_members=request.user)
		context['private_chats'] = private_chats

	else:
		context['authenticated'] = 'no'


	return render(request, 'chat/index.html', context)


# public chat
def public_room(request, **kwargs):

	context = {
		'room_name': kwargs['room_name'],
	}

	if request.user.is_authenticated:
		context['username'] = request.user.username
	else:
		context['username'] = request.session['username']

	return render(request, 'chat/public_room.html', context)

# private chat
@login_required
def private_room(request, **kwargs):

	room_name = kwargs['room_name']

	if request.is_ajax():

		if request.method == "POST":

			if 'messageText' in request.POST:

				message_text = request.POST['messageText']
				message_author = User.objects.get(username=request.POST['messageAuthor'])
				message_chat = PrivateChat.objects.get(chat_name=room_name)

				new_message = Message(text=message_text, author=message_author, chat=message_chat)
				new_message.save();

				timestamp_to_est = new_message.timestamp.astimezone(timezone('US/Eastern'))
				message_timestamp = timestamp_to_est.strftime('%b %-d, %-I:%M %p')

				return JsonResponse({'message_timestamp': message_timestamp}, status=200)


	room = PrivateChat.objects.get(chat_name=room_name)
	room_messages = Message.objects.filter(chat=room)

	context = {
		'room': room,
		'room_messages': room_messages
	}

	if request.user not in room.group_members.all():
		raise PermissionDenied
	else:
		return render(request, 'chat/private_room.html', context)