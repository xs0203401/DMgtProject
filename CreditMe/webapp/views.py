from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone

from .models import Employee, Redemption, Message, Transaction

from datetime import datetime


def get_this_user_employee(request):
	this_user = request.user
	this_employee = Employee.objects.get(user_id=this_user)
	return this_user, this_employee

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='login/')
def index(request):
	this_user, this_employee = get_this_user_employee(request)

	context = {
        'user': this_user,
        'employee': this_employee,
        'datetime': timezone.now().date(),
    }
	return render(request, 'webapp/home.html', context)


@login_required(login_url='login/')
def send(request):
	this_user, this_employee = get_this_user_employee(request)
	# exclude system pk=6
	# exclude this employee's pk.id
	employees = Employee.objects.exclude(pk=6).exclude(pk=this_employee.id)
	
	context = {
        'user': this_user,
        'employee': this_employee,
        'datetime': timezone.now().date(),
        'employees': employees,
    }
	return render(request, 'webapp/send.html', context)

@login_required(login_url='login/')
def redemption(request):
	this_user, this_employee = get_this_user_employee(request)

	rdp_options = Redemption.objects.all()

	context = {
        'user': this_user,
        'employee': this_employee,
        'datetime': timezone.now().date(),
        'rdp_options': rdp_options,
    }
	return render(request, 'webapp/redemption.html', context)