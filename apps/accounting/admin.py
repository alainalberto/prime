from django.contrib import admin

from apps.accounting.models import *

# Register your models here.


admin.site.register(Account)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Invoice)
admin.site.register(Item)
admin.site.register(Receipt)
admin.site.register(Payment)
admin.site.register(Fee)
