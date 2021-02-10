from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('adminsonly/', admin.site.urls),
    path('', include('chat.urls')),
    path('users/', include('users.urls')),
]
