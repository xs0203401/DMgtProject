from django.utils import timezone

from .models import Employee, Redemption, Message, Transaction, Report
from django.contrib.auth.models import User

from datetime import datetime, timedelta
import random

def generate_data(n=20, num_month=1, num_month_ago=0, s_r_percent=0.9, point_per=0.3):
	'''
	n = rows of data
	num_month = number of month(s) in range (default = 1)
	num_month_ago = start from when
	s_r_percent = percent of sending (vs. redemption)
	point_per = the random range of points

	'''
	num_month=int(num_month)
	num_month_ago=int(num_month_ago)
	employees = Employee.objects.exclude(pk=6).all()
	rdm_s = Redemption.objects.all()
	sys_employee = Employee.objects.get(pk=6)
	
	for _ in range(n):
		if random.random()<s_r_percent:
			e_rec = employees[int(random.random()*len(employees))]
			e_send = employees[int(random.random()*len(employees))]

			this_trans = Transaction(
				rec_ID = e_rec,
				send_ID = e_send,
				points = int(random.random()*e_send.point_tosd*point_per+1),
				pub_date = timezone.now()-timedelta(days=int(random.random()*30*num_month+1+30*num_month_ago))
				)
			rnd_msg = Message(
				title = 'Random giving',
				content = 'Generated at: {}'.format(timezone.now())
				)
			rnd_msg.save()
			e_rec.point_recd += this_trans.points
			e_rec.save()
			e_send.point_tosd -= this_trans.points
			e_send.save()
			this_trans.message=rnd_msg
			this_trans.save()
			print(
				this_trans.id,
				this_trans.message.title,
				this_trans.points,
				this_trans.message.content
			)
		else:
			e_send = employees[int(random.random()*len(employees))]
			this_rdm = None
			for rdm in rdm_s:
				if rdm.point_price<e_send.point_recd:
					this_rdm = rdm
					break
			if this_rdm is None: continue

			this_trans = Transaction(
				rec_ID = sys_employee,
				send_ID = e_send,
				pub_date = timezone.now()-timedelta(days=int(random.random()*30*num_month+1+30*num_month_ago))
				)
			this_trans.rdm_ID = this_rdm
			this_trans.points = this_rdm.point_price
			rnd_msg = Message(
				title = 'Random redemption',
				content = 'Generated at: {}'.format(timezone.now())
				)
			rnd_msg.save()
			e_send.point_tosd -= this_trans.points
			e_send.save()
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