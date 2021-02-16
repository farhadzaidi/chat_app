from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='users-sign-up'),
    path('sign-in/', LoginView.as_view(template_name='users/sign-in.html'), name='users-sign-in'),
    path('sign-out/', LogoutView.as_view(template_name='users/sign-out.html'), name='users-sign-out'),
    path('verify-email/<int:pk>/', views.verify_email_view, name='users-verify-email'),

]
