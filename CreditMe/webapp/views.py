from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import datetime

# Create your views here.
@login_required(login_url='login/')
def index(request):
	return render(request, 'webapp/home.html')

def login(request):
	if request.user.is_authenticated:
		return redirect('/')
	else:
		return render(request, 'registration/login.html')