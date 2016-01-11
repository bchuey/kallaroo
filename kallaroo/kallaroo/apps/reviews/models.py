from __future__ import unicode_literals
from django.db import models
from ..accounts.models import User
from ..tasks.models import Task, Bid


# Create your models here.

class Review(models.Model):
	author = models.ForeignKey(User, related_name='review_author')
	comment = models.TextField()
	posted_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	rating = models.IntegerField(null=True, blank=True)
	"""
	can either write a review for the contractor or specific task
	"""
	user = models.ForeignKey(User, null=True, blank=True, related_name='client_reviewer')
	contractor = models.ForeignKey(User, null=True, blank=True, related_name='contractor_reviewer')
	task = models.ForeignKey(Task, null=True, blank=True)

	class Meta:
		db_table = 'reviews'

	def __str__(self):
		return str(self.id)


class Rating(models.Model):
	value = models.IntegerField(default=0, null=True, blank=True)
	"""
	can either write a review for the contractor or specific task
	"""
	user = models.ForeignKey(User, null=True, blank=True, related_name='client_rater')
	contractor = models.ForeignKey(User, null=True, blank=True, related_name='contractor_rater')
	task = models.ForeignKey(Task, null=True, blank=True)

	class Meta:
		db_table = 'ratings'

	def __str__(self):
		return str(self.id)