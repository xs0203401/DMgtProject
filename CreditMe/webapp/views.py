from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone

from .models import Employee, Redemption, Message, Transaction

import datetime

# Create your views here.
@login_required(login_url='login/')
def index(request):
	this_user = request.user
	this_employee = Employee.objects.get(user_id=this_user)

	context = {
        'user': this_user,
        'employee': this_employee,
        'datetime': datetime.now(),
        'timezoned': timezone.now(),
    }
	return render(request, 'webapp/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')