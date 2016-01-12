from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Category(models.Model):
	title = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)

	class Meta:
		db_table = 'categories'

	def __str__(self):
		return str(self.id)

class Subcategory(models.Model):
	title = models.CharField(max_length=255)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	tagline = models.CharField(max_length=255, default="enter a tagline")
	display_img = models.ImageField(null=True, blank=True)

	class Meta:
		db_table = 'subcategories'

	def __str__(self):
		return self.title