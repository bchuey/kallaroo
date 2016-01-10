from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.categories.models import Subcategory
import datetime

class HomepageTemplateView(TemplateView):
	template_name = 'main/index.html'

	def get_context_data(self, **kwargs):
		context = super(HomepageTemplateView, self).get_context_data(**kwargs)
		context['subcategories'] = Subcategory.objects.all()[:6]
		return context

class HowItWorksTemplateView(TemplateView):
	template_name = 'main/how-it-works.html'

class AboutUsTemplateView(TemplateView):
	template_name = 'main/about-us.html'

