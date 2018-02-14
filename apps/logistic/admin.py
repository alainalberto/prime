from django.contrib import admin

from apps.logistic.models import *

# Register your models here.
admin.site.register(Load)
admin.site.register(DriversLogt)
admin.site.register(DispatchLogt)
admin.site.register(Diesel)
admin.site.register(InvoicesHasLoad)
