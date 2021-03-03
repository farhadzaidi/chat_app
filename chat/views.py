from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile, FriendRequest
from django.contrib import messages
from django.http import JsonResponse
from .models import Message, PrivateChat, PrivateChatInvitation
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from pytz import timezone
from django.core.exceptions import PermissionDenied
import re

def get_context(request, **kwargs):
	kwargs['context'] = {}
	kwargs['context']['name'] = 'Farhad'
	return kwargs

def notification_requests(request, **kwargs):

	if request.is_ajax():
		if request.method == 'POST':
			if 'text' in request.POST:

				return JsonResponse({}, status=200)


def notification_decorator(func):

	def wrapper(*args, **kwargs):

		kwargs = get_context(*args, **kwargs)

		notification_requests(*args, **kwargs)

		return func(*args, **kwargs)


	return wrapper


@notification_decorator
def index_view(request, **kwargs):

	new_context = kwargs['context']
	# print(new_context['name'])	
	# AJAX requests
	if request.is_ajax():

		# AJAX POST requests
		if request.method == 'POST':

			# send friend request
			if 'friendName' in request.POST:

				sender = request.user
				reciever = User.objects.get(username=request.POST['friendName'])

				friend_request = FriendRequest(sender=sender, reciever=reciever)
				friend_request.save()

				messages.success(request, f'Friend request sent to {reciever}')

				return JsonResponse({}, status=200)

			# TODO: needs to be universal
			# accept friend request
			if 'acceptFriendPK' in request.POST:

				sender = User.objects.get(pk=request.POST['acceptFriendPK'])
				reciever = request.user

				sender.profile.friends.add(reciever)
				reciever.profile.friends.add(sender)

				friend_request = FriendRequest.objects.get(sender=sender, reciever=reciever)
				friend_request.delete()

				messages.success(request, f'You and {sender} are now friends!')

				return JsonResponse({}, status=200)

			# TODO: needs to be universal
			# decline friend request
			if 'declineFriendPK' in request.POST:

				sender = User.objects.get(pk=request.POST['declineFriendPK'])
				reciever = request.user

				friend_request = FriendRequest.objects.get(sender=sender, reciever=reciever)
				friend_request.delete()

				return JsonResponse({}, status=200)

			# create private chat
			if 'chatName' in request.POST:

				chat_name = get_random_string(length=16)
				chat_alias = request.POST['chatName']

				new_private_chat = PrivateChat(name=chat_name, alias=chat_alias)
				new_private_chat.save()
				new_private_chat.members.add(request.user)
				new_private_chat.save()

				new_private_chat.save()

				invite_friends = request.POST.getlist('inviteFriends[]')

				for friend in invite_friends:
					reciever = User.objects.get(username=friend)
					new_invitation = PrivateChatInvitation(sender=request.user, reciever=reciever, chat=new_private_chat)
					new_invitation.save()

				messages.success(request, f'{new_private_chat} created and invitations sent out.')

				return JsonResponse({}, status=200)

			# TODO: needs to be universal
			if 'acceptInvitation' in request.POST:

				private_chat = PrivateChat.objects.get(pk=request.POST['acceptInvitation'])
				private_chat.members.add(request.user)

				invitation = PrivateChatInvitation.objects.get(chat=private_chat, reciever=request.user)
				invitation.delete()

				messages.success(request, f'You are now a part of {private_chat}')

				return JsonResponse({}, status=200)

			# TODO: needs to be universal
			if 'declineInvitation' in request.POST:

				private_chat = PrivateChat.objects.get(pk=request.POST['declineInvitation'])

				invitation = PrivateChatInvitation.objects.get(chat=private_chat, reciever=request.user)
				invitation.delete()

				return JsonResponse({}, status=200)


		# AJAX GET requests
		data = {}

		if 'getInfo' in request.GET: 
			
			# get all usernames in database 
			usernames = [user.username for user in User.objects.all()]
			data['usernames'] = usernames

			# get current user's friends list
			friends = request.user.profile.friends.all()
			friends_list = [friend.username for friend in friends]
			data['friends_list'] = friends_list

			# get current user's sent friend requests
			friend_requests = FriendRequest.objects.filter(sender=request.user)
			pending_friend_requests = [friend_request.reciever.username for friend_request in friend_requests]
			data['pending_friend_requests'] = pending_friend_requests

			# get primary keys of users who sent friend requests to the current user
			friend_requests = FriendRequest.objects.filter(reciever=request.user)
			friend_request_pks = [friend_req.sender.pk for friend_req in friend_requests]
			data['friend_request_pks'] = friend_request_pks

			# get primary keys of user who sent private chat invitations to the current user
			chat_invitations = PrivateChatInvitation.objects.filter(reciever=request.user)
			chat_invitation_pks = [chat.chat.pk for chat in chat_invitations]
			data['chat_invitation_pks'] = chat_invitation_pks

			# get names of user's private chats
			private_chats = PrivateChat.objects.filter(members=request.user)
			private_chat_names = [chat.alias for chat in private_chats]
			data['private_chat_names'] = private_chat_names


		return JsonResponse(data, status=200)



	# POST requests
	if request.method == 'POST':

		# enter public chat
		if 'chat-name' in request.POST:
			chat_name = request.POST['chat-name']

			regex = '^[a-zA-Z0-9]+$'

			if re.match(regex, chat_name):

				username = request.POST['username']

				request.session['username'] = username

				return redirect(reverse('public-chat', kwargs={'chat_name': chat_name}))

			else:
				messages.error(request, 'The chat name must contain only alphanumeric characters and must not contain any spaces.')
				return redirect('chat-index')

	# GET requests
	context = {
		'title': 'Home',
	}

	if request.user.is_authenticated:

		private_chats = PrivateChat.objects.filter(members=request.user)
		context['private_chats'] = private_chats

		chat_invitations = PrivateChatInvitation.objects.filter(reciever=request.user)
		context['chat_invitations'] = chat_invitations

		friend_requests = FriendRequest.objects.filter(reciever=request.user)
		context['friend_requests'] = friend_requests

	return render(request, 'chat/index.html', context)


# public chat
def public_chat_view(request, **kwargs):

	context = {
		'chat_name': kwargs['chat_name'],
	}

	if request.user.is_authenticated:
		context['username'] = request.user.username
	else:
		context['username'] = request.session['username']

	return render(request, 'chat/public_chat.html', context)

# private chat
@login_required
def private_chat_view(request, **kwargs):

	chat_name = kwargs['chat_name']

	if request.is_ajax():

		if request.method == "POST":

			if 'messageText' in request.POST:

				message_text = request.POST['messageText']
				message_author = User.objects.get(username=request.POST['messageAuthor'])
				message_chat = PrivateChat.objects.get(name=chat_name)

				new_message = Message(text=message_text, author=message_author, chat=message_chat)
				new_message.save();

				timestamp_to_est = new_message.timestamp.astimezone(timezone('US/Eastern'))
				message_timestamp = timestamp_to_est.strftime('%b %-d, %-I:%M %p')

				return JsonResponse({'message_timestamp': message_timestamp}, status=200)

			if 'inviteFriends[]' in request.POST:

				invite_friends = request.POST.getlist('inviteFriends[]')
				
				for friend in invite_friends:
					reciever = User.objects.get(username=friend)
					chat = PrivateChat.objects.get(name=chat_name)
					new_invitation = PrivateChatInvitation(sender=request.user, reciever=reciever, chat=chat)
					new_invitation.save()

				return JsonResponse({}, status=200)

		data = {}

		if 'getInfo' in request.GET:
			chat = PrivateChat.objects.get(name=chat_name)
			invitations_sent = PrivateChatInvitation.objects.filter(chat=chat)
			friends_sent_to = [invitation.reciever.username for invitation in invitations_sent]
			data['friends_sent_to'] = friends_sent_to

		return JsonResponse(data, status=200)			


	chat = PrivateChat.objects.get(name=chat_name)
	chat_messages = Message.objects.filter(chat=chat)

	context = {
		'chat': chat,
		'chat_messages': chat_messages
	}

	if request.user not in chat.members.all():
		raise PermissionDenied
	else:
		return render(request, 'chat/private_chat.html', context)
