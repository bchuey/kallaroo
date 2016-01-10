from __future__ import unicode_literals

from django.db import models
from ..accounts.models import User, Contractor
from ..categories.models import Subcategory
# from ..reviews.models import Review, Rating

class Task(models.Model):
	TASK_STATUS = (

		('Open', 'Open'),
		('Active', 'Active'),
		('Completed', 'Completed'),
		('Paid', 'Paid'),
	)
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	contractor = models.ForeignKey(Contractor, blank=True, null=True)
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	special_instructions = models.TextField(blank=True, null=True)
	task_status = models.CharField(max_length=30, choices=TASK_STATUS, default='Open')
	is_completed = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	bidding_closed_at = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
	task_completed_at = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
	final_bid = models.OneToOneField('Bid', null=True, blank=True, related_name='final_bid')
	task_img = models.ImageField(null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)
	lng = models.FloatField(null=True,blank=True)
	lat = models.FloatField(null=True,blank=True)
	final_rating = models.IntegerField(default=0, null=True, blank=True)

	# additional attributes to keep track of the total time and payment fee
	task_clock_in = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
	task_clock_out = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
	final_payment = models.DecimalField(max_digits=999, decimal_places=2, null=True, blank=True)



	"""
	a subcategory contains many tasks;
	subcategory_id in the user table 
	"""
	subcategory = models.ForeignKey(Subcategory, null=True, blank=True)


	class Meta:
		db_table = 'tasks'

	def __str__(self):
		return self.title

class Bid(models.Model):
	BID_CHOICES = (

		('Hourly', 'Hourly'),
		('Project', 'Project'),

	)
	contractor = models.ForeignKey(Contractor)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	is_accepted = models.BooleanField(default=False)
	bid_type = models.CharField(max_length=20, choices=BID_CHOICES, default='Hourly')
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	estimated_hours = models.IntegerField(default=1, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
	accepted_at = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)


	class Meta:
		db_table = 'bids'

	def __str__(self):
		return str(self.id)

"""
Bid serializer 
"""
from rest_framework import serializers

class BidSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bid
		fields = ('contractor', 'task', 'bid_type', 'amount', 'estimated_hours')
		depth = 1


class Location(models.Model):
	STATE_CHOICES = (
		('AZ', 'AZ'),
		('CA', 'CA'),
		('TX', 'TX'),
	)
	street_number = models.IntegerField()
	street_address = models.CharField(max_length=60)
	city = models.CharField(max_length=60)
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='AZ')
	zipcode = models.IntegerField()
	task = models.ForeignKey(Task, on_delete=models.CASCADE)

	class Meta:
		db_table = 'locations'

	def __str__(self):
		return self.get_location()

	def get_location(self):
		return "%s %s, %s, %s, %s" %(self.street_number, self.street_address, self.city, self.state, self.zipcode)


