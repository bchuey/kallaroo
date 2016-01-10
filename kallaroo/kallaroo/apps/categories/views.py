from django.shortcuts import render
from .models import Category, Subcategory
from django.views.generic.edit import CreateView
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from ..tasks.models import Task
from ..accounts.models import ContractorProfile

# Create your views here.

class SubcategoryListView(ListView):
	model = Subcategory
	template_name = 'categories/subcategory_list.html'

class SubcategoryDetailView(DetailView):
	model = Subcategory
	template_name = 'categories/partials/subcategory_detail.html'

	def get_context_data(self, **kwargs):
		context = super(SubcategoryDetailView, self).get_context_data(**kwargs)
		context['tasks'] = Task.objects.filter(subcategory=self.object)
		context['contractors'] = ContractorProfile.objects.filter(subcategory=self.object)
		return context

class SubcategoryTaskDetailView(DetailView):
	model = Subcategory
	template_name = 'categories/partials/subcategory/tasks.html'

	def get_context_data(self, **kwargs):
		context = super(SubcategoryTaskDetailView, self).get_context_data(**kwargs)
		context['tasks'] = Task.objects.filter(subcategory=self.object)
		return context

class SubcategoryContractorDetailView(DetailView):
	model = Subcategory
	template_name = 'categories/partials/subcategory/contractors.html'

	def get_context_data(self, **kwargs):
		context = super(SubcategoryContractorDetailView, self).get_context_data(**kwargs)
		context['contractors'] = ContractorProfile.objects.filter(subcategory=self.object)
		return context