import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    point_recd = models.IntegerField(default=0)
    point_tosd = models.IntegerField(default=1000)
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=128)


class Transaction(models.Model):
	rec_ID = models.ForeignKey(Employee, on_delete=models.CASCADE)
	send_ID = models.ForeignKey(Employee, on_delete=models.CASCADE)
	points = models.IntegerField(default=0)
	message = models.ForeignKey(Message, on_delete=models.CASCADE)
	rdm_ID = model.ForeignKey(Redemption, on_delete=models.CASCADE)
	pub_date = models.DateTimeField('transaction date stamp')

class Redemption(models.Model):
	point_price = models.IntegerField(default=100)
	title = models.CharField(max_length=64)

class Message(models.Model):
	title = models.CharField(max_length=80)
	content = models.CharField(max_length=240)
