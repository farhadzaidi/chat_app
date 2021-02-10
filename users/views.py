from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

def sign_up_view(request):

	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save(commit=False)
			new_user.customuser = CustomUser(user=new_user)
			new_user.save()
			return redirect('chat-index')


	context = {
		'title': 'Sign Up',
		'form': UserCreationForm(),
	}
	return render(request, 'users/sign-up.html', context)

