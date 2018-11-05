from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone

from .models import Employee, Redemption, Message, Transaction

from datetime import datetime

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('/')

def get_this_user_employee():
	this_user = request.user
	this_employee = Employee.objects.get(user_id=this_user)
	return this_user, this_employee

@login_required(login_url='login/')
def index(request):
	this_user, this_employee = get_this_user_employee()

	context = {
        'user': this_user,
        'employee': this_employee,
        'datetime': timezone.now().date(),
    }
	return render(request, 'webapp/home.html', context)


@login_required(login_url='login/')
def send(request):
	this_user, this_employee = get_this_user_employee()
	employees = Employee.objects.exclude(pk=e1.id)


	context = {
        'user': this_user,
        'employee': this_employee,
        'employees': employees,
        'datetime': timezone.now().date(),
    }
	return render(request, 'webapp/send.html', context)