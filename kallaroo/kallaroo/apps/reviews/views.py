from django.shortcuts import render
from . models import Review, Rating
from . forms import CreateReviewForm, CreateRatingForm
from ..accounts.models import User
from ..tasks.models import Task
from django.views.generic.edit import CreateView
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Create your views here.
class AddTaskReview(CreateView):
	model = Review
	template_name = 'reviews/create_task_review.html'
	form = CreateReviewForm
	fields = ('comment', 'rating')
	success_url = '/tasks'

	"""
	1.) ASSIGNING the author to request.user
	2.) PASSING the url parameter to be used to fetch specific task 
	"""
	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.task = Task.objects.get(pk=self.kwargs['task_id'])
		return super(AddTaskReview, self).form_valid(form)


class AddTaskRating(CreateView):
	model = Rating
	template_name = 'reviews/create_task_rating.html'
	form = CreateRatingForm
	fields = ('value')
	success_url = '/tasks'

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.task = Task.objects.get(pk=self.kwargs['task_id'])
		return super(AddTaskRating, self).form_valid(form)



# class AddContractorReview(CreateView):
# 	model = Review
# 	template_name = 'reviews/create_contractor_review.html'
# 	form = CreateReviewForm
# 	fields = ('comment', 'rating')
# 	success_url = '/tasks'

# 	"""
# 	1.) ASSIGNING the author to request.user
# 	2.) PASSING the url parameter to be used to fetch specific contractor 
# 	"""
# 	def form_valid(self, form):
# 		form.instance.author = self.request.user
# 		form.instance.contractor = Contractor.objects.get(pk=self.kwargs['contractor_id'])
# 		return super(AddContractorReview, self).form_valid(form)

# class AddContractorRating(CreateView):
# 	model = Rating
# 	template_name = 'reviews/create_contractor_rating.html'
# 	form = CreateRatingForm
# 	fields = ('value')
# 	success_url = '/tasks'

# 	def form_valid(self, form):
# 		form.instance.author = self.request.user
# 		form.instance.contractor = Contractor.objects.get(pk=self.kwargs['contractor_id'])
# 		return super(AddContractorRating, self).form_valid(form)