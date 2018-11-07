import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    point_recd = models.IntegerField(default=0)
    point_tosd = models.IntegerField(default=1000)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

class Redemption(models.Model):
	point_price = models.IntegerField(default=100)
	title = models.CharField(max_length=64)

class Message(models.Model):
	title = models.CharField(max_length=80)
	content = models.CharField(max_length=240)

class Transaction(models.Model):
	rec_ID = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='receiver')
	send_ID = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='sender')
	points = models.IntegerField(default=0)
	message = models.ForeignKey(Message, on_delete=models.CASCADE, blank=True, null=True)
	rdm_ID = models.ForeignKey(Redemption, on_delete=models.CASCADE, blank=True, null=True)
	pub_date = models.DateTimeField('transaction date stamp')

class Report(models.Model):
	title = models.CharField(max_length=100)
	sql_string = models.CharField(default='select 0')