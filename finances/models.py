from django.conf import settings
from django.db import models

class Asset(models.Model):
	asset_type = models.CharField(max_length=20)
	description = models.CharField(max_length=200)
	value = models.PositiveIntegerField()
	active = models.BooleanField(default=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def __str__(self):
		return self.description

class MonthlyStatement(models.Model):
	month_year = models.DateField()
	salary = models.PositiveIntegerField()
	expenses = models.PositiveIntegerField()
	savings = models.PositiveIntegerField()
	liquid = models.PositiveIntegerField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def  __str__(self):
		return 'Monthly statement for user: {}, {}, {}'.format(self.user.username, self.month_year.month, self.month_year.year)

	class Meta:
		unique_together = ('user', 'month_year',)

