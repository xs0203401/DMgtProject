from django.contrib import admin
from .models import Employee, Redemption, Message, Transaction, Report

# Register your models here.
admin.site.register(Employee)
admin.site.register(Redemption)
admin.site.register(Message)
admin.site.register(Transaction)
admin.site.register(Report)