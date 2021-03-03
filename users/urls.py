from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
  LoginView, LogoutView,
  PasswordChangeView,
  PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='users-sign-up'),
    path('sign-in/', LoginView.as_view(template_name='users/sign-in.html'), name='users-sign-in'),
    path('sign-out/', LogoutView.as_view(template_name='users/sign-out.html'), name='users-sign-out'),
    
    path('verify-email/<int:pk>/', views.verify_email_view, name='users-verify-email'),
   	path('resend-verification-email/', views.resend_verification_email_view, name='users-resend-verification-email'),
    
    path('forgot-username/', views.forgot_username_view, name='users-forgot-username'),
    
    path('password-change/', PasswordChangeView.as_view(template_name='users/password-change.html', extra_context={'title': 'Password Change'}, success_url=reverse_lazy('users-password-change-done')), name='users-password-change'),
    path('password-change-done/', views.password_change_done_view, name='users-password-change-done'),
   	
    path('password-reset/', PasswordResetView.as_view(template_name='users/password-reset.html', extra_context={'title': 'Reset Password'}), name='users-password-reset'),
   	path('password-reset-done/', PasswordResetDoneView.as_view(template_name='users/password-reset-done.html', extra_context={'title': 'Password Reset Sent'}), name='password_reset_done'),
   	path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password-reset-confirm.html', extra_context={'title': 'New Password'}), name='password_reset_confirm'),
   	path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='users/password-reset-complete.html', extra_context={'title': 'Password Reset Complete'}), name='password_reset_complete'),

    path('account-delete/', views.account_delete_view, name='users-account-delete'),
]