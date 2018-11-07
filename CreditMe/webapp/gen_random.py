from django.utils import timezone

from .models import Employee, Redemption, Message, Transaction, Report
from django.contrib.auth.models import User

from datetime import datetime, timedelta
import random

def generate_data(n, num_month=2, num_month_ago=0, percent=0.80, point_range=300):
	'''
	n = rows of data
	num_month = number of month(s) in range
	num_month_ago = start from when
	percent = percent of sending (vs. redemption)
	point_range = the random range of points

	this generator does not change points in employees' accounts
	'''
	num_month=int(num_month)
	num_month_ago=int(num_month_ago)
	employees = Employee.objects.exclude(pk=6).all()
	rdm_s = Redemption.objects.all()
	
	for _ in range(n):
		if random.random()<percent:
			this_trans = Transaction(
				rec_ID = employees[int(random.random()*len(employees))],
				send_ID = employees[int(random.random()*len(employees))],
				points = int(random.random()*point_range+1),
				pub_date = timezone.now()-timedelta(days=int(random.random()*30*num_month+1+30*num_month_ago))
				)
			rnd_msg = Message(
				title = 'Random giving',
				content = 'Generated at: {}'.format(timezone.now())
				)
			rnd_msg.save()
			this_trans.message=rnd_msg
			this_trans.save()
			print(
				this_trans.id,
				this_trans.message.title,
				this_trans.points,
				this_trans.message.content
			)
		else:
			this_trans = Transaction(
				rec_ID = employees[int(random.random()*len(employees))],
				send_ID = employees[int(random.random()*len(employees))],
				pub_date = timezone.now()-timedelta(days=int(random.random()*30*num_month+1+30*num_month_ago))
				)
			this_rdm = rdm_s[int(random.random()*len(rdm_s))]
			this_trans.rdm_ID = this_rdm
			this_trans.points = this_rdm.point_price
			rnd_msg = Message(
				title = 'Random redemption',
				content = 'Generated at: {}'.format(timezone.now())
				)
			rnd_msg.save()
			this_trans.message=rnd_msg
			this_trans.save()
			print(
				this_trans.id,
				this_trans.message.title,
				this_trans.points,
				this_trans.message.content,
				this_trans.rdm_ID.title
			)

# System user id = 1
# System employee id = 6