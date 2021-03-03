from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import UpdateView

def sign_up_view(request):

	if request.method == "POST":
		form = UserCreationForm(request.POST)

		if form.is_valid():
			# save user to database
			new_user = form.save()

			# authenticate and log user in
			username = request.POST['username']
			password = request.POST['password1']
			user = authenticate(request, username=username, password=password)
			login(request, user)

			# create a profile for the user
			new_user.profile = Profile(user=new_user)

			# if user enters their email, send a verification email and notifiy user
			if request.POST['email']:
				# save user's email as an unverified email in the database
				# this is so that it does not get saved as the user's actual email, but can be fetched later 
				new_user.profile.unverified_email = request.POST['email']

				# info for verification email
				pk = request.user.pk
				domain = request.META['HTTP_HOST']

				# construct verification email 
				subject = 'Verify your email'
				message = f'''\
				Hi {username},
				Thanks for creating an account on my chat application.
				Click the following link to verify your email address:
				http://{domain}/users/verify-email/{pk}/
				'''
				sender = 'zaidi.farhad03@gmail.com'
				recipient = [request.POST['email']]

				# context for html message
				email_context = {
					'username': username,
					'pk': pk,
					'domain': domain,
					}
				html_message = render_to_string('users/email_templates/verification_email.html', email_context)

				# send verification email
				send_mail(subject, message, sender, recipient, html_message=html_message)

				# notify user
				messages.info(request, 'A verification email has been sent to your email address.')
			else:
				messages.success(request, 'Account created successfully!')

			new_user.profile.save()
			return redirect('chat-index')


	context = {
		'title': 'Sign Up',
		'form': UserCreationForm(),
		}
	return render(request, 'users/sign-up.html', context)

@login_required
def verify_email_view(request, **kwargs):
	pk = kwargs['pk']
	if request.user.pk == pk and request.user.profile.unverified_email != '':

		user = request.user
		email = user.profile.unverified_email
		user.email = email
		user.profile.unverified_email = ''
		user.save()
		user.profile.save()

		messages.success(request, 'Your email has been verified and is now associated with your account!')
		return redirect('chat-index')

	else:
		raise PermissionDenied

def resend_verification_email_view(request):

	# info for verification email
	username = request.user.username
	pk = request.user.pk
	domain = request.META['HTTP_HOST']

	# construct verification email 
	subject = 'Verify your email'
	message = f'''\
	Hi {username},
	Thanks for creating an account on my chat application.
	Click the following link to verify your email address:
	http://{domain}/users/verify-email/{pk}/
	'''
	sender = 'zaidi.farhad03@gmail.com'
	recipient = [request.user.profile.unverified_email]

	# context for html message
	email_context = {
		'username': username,
		'pk': pk,
		'domain': domain,
		}
	html_message = render_to_string('users/email_templates/verification_email.html', email_context)

	# send verification email
	send_mail(subject, message, sender, recipient, html_message=html_message)

	return redirect('chat-index')

def forgot_username_view(request):

	if request.method == 'POST':

		email = request.POST['email']
		username = User.objects.get(email=email)
		domain = request.META['HTTP_HOST']
 
		subject = 'Chat - Recover Username'
		message = f'''\n
		Your username is {username}.
		Click the following link to return to the sign in page: 
		http://{domain}/users/sign-in/
		'''
		sender = 'zaidi.farhad03@gmail.com'
		recipient = [email]

		send_mail(subject, message, sender, recipient)

		messages.info(request, 'An email has been sent to your email address with your username.')
		return redirect('users-sign-in')

	return render(request, 'users/forgot-username.html')

def password_change_done_view(request):
	messages.success(request, 'Your password has been changed.')
	logout(request)

	return redirect('users-sign-in')

def account_delete_view(request):

	if request.method == "POST":
		request.user.delete()
		messages.info(request, 'Account Deleted.')
		return redirect('chat-index')


	return render(request, 'users/account-delete.html', {'title': 'Delete Account'})

