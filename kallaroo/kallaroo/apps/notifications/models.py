from __future__ import unicode_literals
from django.db import models

from ..accounts.models import User
from ..tasks.models import Task
# Create your models here.

class Notification(models.Model):
	msg = models.TextField()
	sent_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	# contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)

	class Meta:
		db_table = 'notifications'

	def __str__(self):
		return str(self.id)