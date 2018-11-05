from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Employee, Redemption, Message, Transaction

import datetime

# Create your views here.
@login_required(login_url='login/')
def index(request):
	this_user = request.user
	print(this_user.id)
	# this_employee = Employee.

	context = {
        # 'question': question,
        # 'error_message': "You didn't select a choice.",
    }
	return render(request, 'webapp/home.html')

