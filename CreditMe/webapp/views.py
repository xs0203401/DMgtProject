from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone

from .models import Employee, Redemption, Message, Transaction
from django.contrib.auth.models import User

from datetime import datetime

TRANS_STATUS={
	'SUCCESS':0,
	'ILLEGAL':1,
	'INSUFFICIENT':2
}

def get_this_user_employee(request):
	this_user = request.user
	this_employee = Employee.objects.get(user_id=this_user)
	return this_user, this_employee

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def index(request):
	this_user, this_employee = get_this_user_employee(request)

	context = {
        'user': this_user,
        'employee': this_employee,
        'datetime': timezone.now().date(),
    }
	return render(request, 'webapp/home.html', context)


@login_required(login_url='/login/')
def send(request):
	if request.method == 'POST':
		# <QueryDict: {'msg_content': ['ccc'], 'csrfmiddlewaretoken': ['JDs57HliW4SDzNaW2KOqjSDOupRxQ9
		# duv2kmqNER4GzLDg7JoLkJVYlmebSMlafT'], 'msg_title': ['yttt'], 'points': ['15'], 'rec_user': [
		# 'henryliu']}>
		
		# get receiver and sender
		this_user = request.user
		send_employee = Employee.objects.get(user_id=this_user)
		try:
			rec_user = User.objects.get(pk=int(request.POST['rec_user']))
			rec_employee = Employee.objects.get(user_id=rec_user)
		except:
			return redirect('/send?status={}'.format(TRANS_STATUS['ILLEGAL']))

		# get transaction
		try:
			trans_points = int(request.POST['points'])
		except:
			return redirect('/send?status={}'.format(TRANS_STATUS['ILLEGAL']))

		if trans_points <= 0:
			return redirect('/send?status={}'.format(TRANS_STATUS['ILLEGAL']))

		# check if point sufficient
		if send_employee.point_tosd <= trans_points:
			return redirect('/send?status={}'.format(TRANS_STATUS['INSUFFICIENT']))

		# transaction is legal
		# Record transaction
		this_trans = Transaction(
			rec_ID = rec_employee,
			send_ID = send_employee,
			points = trans_points,
			pub_date = timezone.now()
			)

		# if there is message information save message
		if request.POST['msg_title']!='' or request.POST['msg_content']!='':
			# create and save message
			trans_msg = Message(
				title = str(request.POST['msg_title']),
				content = str(request.POST['msg_content'])
				)
			trans_msg.save()
			# key transaction
			this_trans.message = trans_msg
		# change sender points
		send_employee.point_tosd -= trans_points
		# change receiver points
		rec_employee.point_recd += trans_points
		
		# Close transaction
		# save transaction record
		this_trans.save()
		send_employee.save()
		rec_employee.save()

		# return success status
		return redirect('/send?status={}'.format(TRANS_STATUS['SUCCESS']))

	elif request.method == 'GET':

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

@login_required(login_url='/login/')
def redemption(request):
	if request.method == 'POST':
		# <QueryDict: {'rdp_id': ['1'], 'csrfmiddlewaretoken': ['bWtXhAUY4nNf3WT7ZWLX3QpTRZM9439bXll
		# eAGdxcZun7pQUlXhgFW7rBLNoz4bA']}>
		# print(request.POST)

		# get system employee
		sys_employee = Employee.objects.get(pk=6) # system pk=6
		
		# get this user
		this_user = request.user
		this_employee = Employee.objects.get(user_id=this_user)
		
		# get redemption item
		try:
			rdp_item = Redemption.objects.get(pk=int(request.POST['rdp_id']))
		except:
			return redirect('/redemption?status={}'.format(TRANS_STATUS['ILLEGAL']))
		trans_points = rdp_item.point_price

		# check if point sufficient
		if this_employee.point_recd <= trans_points:
			return redirect('/redemption?status={}'.format(TRANS_STATUS['INSUFFICIENT']))

		# transaction is legal
		# Record transaction
		this_trans=Transaction(
			rec_ID=sys_employee,
			send_ID=this_employee,
			points=trans_points,
			rdm_ID=rdp_item,
			pub_date=timezone.now()
			)
		this_employee.point_recd -= trans_points

		# Close transaction
		# save objects
		this_trans.save()
		this_employee.save()

		# return success status
		return redirect('/redemption?status={}'.format(TRANS_STATUS['SUCCESS']))

	elif request.method == 'GET':

		this_user, this_employee = get_this_user_employee(request)

		rdp_options = Redemption.objects.all()

		context = {
	        'user': this_user,
	        'employee': this_employee,
	        'datetime': timezone.now().date(),
	        'rdp_options': rdp_options,
	    }

		return render(request, 'webapp/redemption.html', context)