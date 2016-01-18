from django.shortcuts import render
from . models import Review, Rating
from . forms import CreateReviewForm, CreateRatingForm
from ..accounts.models import User
from ..tasks.models import Task
from django.views.generic.edit import CreateView
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
def add_review(request):
	form = CreateReviewForm(request.POST or None)
	if request.method == "POST":
		# if form.is_valid():
		author = request.user
		try:
			reviewee = User.objects.get(id=request.POST['reviewee_id'])
		except:
			pass
		comment = request.POST['comment']
		rating = request.POST['rating']
		task = Task.objects.get(id=request.POST['task_id'])

		new_review = Review()
		new_review.author = author
		try:
			new_review.reviewee = reviewee
		except: 
			pass
		new_review.comment = comment
		new_review.rating = rating
		new_review.task = task

		new_review.save()

		return HttpResponseRedirect('%s'%(reverse('tasks:task_detail', args=[task.id])))
