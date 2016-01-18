from __future__ import unicode_literals
from django.db import models
from ..accounts.models import User
from ..tasks.models import Task, Bid


# Create your models here.

class Review(models.Model):
	RATING_CHOICES = (

		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),

	)
	author = models.ForeignKey(User, related_name='author')
	reviewee = models.ForeignKey(User, null=True, blank=True, related_name='reviewee')
	comment = models.TextField()
	posted_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	# rating = models.OneToOneField('Rating', null=True, blank=True)
	rating = models.IntegerField(default=1, choices=RATING_CHOICES, blank=True)
	task = models.ForeignKey(Task, null=True, blank=True)

	class Meta:
		db_table = 'reviews'

	def __str__(self):
		return str(self.id)


class Rating(models.Model):
	RATING_CHOICES = (

		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),

	)

	value = models.IntegerField(default=0, null=True, blank=True, choices=RATING_CHOICES)
	# user = models.ForeignKey(User, null=True, blank=True)
	task = models.ForeignKey(Task, null=True, blank=True)

	class Meta:
		db_table = 'ratings'

	def __str__(self):
		return str(self.id)