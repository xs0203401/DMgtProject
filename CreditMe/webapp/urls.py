from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	path('', views.index, name='index'),
	path('send/', views.send, name='send')
	path('login/', auth_views.LoginView.as_view()),
	path('logout/', views.logout_view, name='logout'),
]