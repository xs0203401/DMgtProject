from django.contrib import admin
from .models import Employee, Redemption, Message, Transaction

# Register your models here.
admin.site.register(Employee)
admin.site.register(Redemption)
admin.site.register(Message)
admin.site.register(Transaction)