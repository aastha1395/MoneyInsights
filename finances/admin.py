from django.contrib import admin

from .models import Asset, MonthlyStatement

admin.site.register(Asset)
admin.site.register(MonthlyStatement)
