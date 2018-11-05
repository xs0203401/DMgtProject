from django.http import HttpResponse
from django.shortcuts import render
import datetime

# Create your views here.
def index(request):
	return render(request, 'webapp/home.html')

def login(request):
	return render(request, 'webapp/login.html')