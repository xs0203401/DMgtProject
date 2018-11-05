from django.http import HttpResponse
from django.shortcuts import render
import datetime

# Create your views here.
@login_required(redirect_field_name='login/')
def index(request):
	return render(request, 'webapp/home.html')

def login(request):
	return render(request, 'webapp/login.html')