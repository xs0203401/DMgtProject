from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import datetime

# Create your views here.
@login_required()
def index(request):
	this_user = request.user

	# this_employee = 

	context = {
        'question': question,
        'error_message': "You didn't select a choice.",
    }
	return render(request, 'webapp/home.html')

