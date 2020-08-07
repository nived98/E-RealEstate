from django.contrib import admin
from .models import Invoice, BankApi

# Register your models here.
admin.site.register(Invoice)
admin.site.register(BankApi)
