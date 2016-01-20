from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import CreateTaskForm, CreateBidForm, ChooseSubcategoryForm, SetAddressForm, AddTaskDetailsForm
from .models import Task, Bid, BidSerializer, Location
from ..accounts.models import User
from ..reviews.forms import CreateReviewForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# import datetime
from django.utils import timezone
from ..categories.models import Subcategory
from formtools.wizard.views import NamedUrlSessionWizardView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
import redis
import json
import stripe

import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
    merchant_id=settings.BRAINTREE_MERCHANT_ID,
    public_key=settings.BRAINTREE_PUBLIC,
    private_key=settings.BRAINTREE_PRIVATE,
)


"""
==================
WizardView 
==================

FORMS = [("name_of_step", form_class)]

TEMPLATES = [("name_of_corresponding_step": "html_page")]

"""

FORMS = [("subcategory", ChooseSubcategoryForm),
					("address", SetAddressForm),
					("details", AddTaskDetailsForm),]

TEMPLATES = {"subcategory": "tasks/create_task_form/step1.html",
						"address": "tasks/create_task_form/step2.html",
						"details": "tasks/create_task_form/step3.html",
}
class AddTaskWizard(NamedUrlSessionWizardView):

	form_list = [ChooseSubcategoryForm, SetAddressForm, AddTaskDetailsForm]

	def get_template_names(self):
		return [TEMPLATES[self.steps.current]]

	def get_form_instance(self, step):
		return self.instance_dict.get(step, None)

	def done(self, form_list, form_dict, **kwargs):
		# do something with the form data(form_list)
		user = self.request.user
		# print("============")
		# print(user)
		# print("============")

		new_task = Task()
		new_task.user = user
		new_task.subcategory = Subcategory.objects.get(id=form_dict['subcategory']['subcategory'].value())

		new_task.address = form_dict['address']['address'].value()

		new_task.title = form_dict['details']['title'].value()

		new_task.description = form_dict['details']['description'].value()

		new_task.special_instructions = form_dict['details']['special_instructions'].value()

		new_task.save()

		"""
		Redis Notifications
		"""
		r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

		context = user.username + " posted a new task in " + new_task.subcategory.title
		
		# channel = new_task.subcategory.title + "_channel"
		channel = "new_task_1"
		# print("the redis channel is: " + channel)
		print context

		r.publish(channel, context)


		return HttpResponseRedirect('%s'%(reverse('tasks:task_list')))


class SuccessView(TemplateView):

	template_name = 'tasks/success.html'

"""
Users should only be able to see their own tasks within their dashboard(?)
"""

class TaskListView(ListView):
	
	model = Task
	template_name = 'tasks/task_list.html'

class TaskDetailView(DetailView):
	model = Task
	template_name = 'tasks/task_detail.html'
	form = CreateBidForm

	def get_context_data(self, **kwargs):
		context = super(TaskDetailView, self).get_context_data(**kwargs)
		context['bid_form'] = self.form()
		context['bids'] = self.object.bid_set.all()
		context['reviews'] = self.object.review_set.all()
		context['review_form'] = CreateReviewForm
		try:
			context['location'] = Location.objects.get(task=self.object)
		except:
			pass
		return context

	def post(self, request, pk):

		form = self.form(request.POST)
		if request.method == 'POST':
			if form.is_valid():
				
				contractor = User.objects.get(id=request.session['user_id'])
				task = Task.objects.get(id=request.POST['task_id'])
				bid_type = request.POST['bid_type']
				amount = request.POST['amount']
				estimated_hours = request.POST['estimated_hours']

				bid = Bid.objects.create(contractor=contractor, task=task, bid_type=bid_type, amount=amount, estimated_hours=estimated_hours)
				# new_bid = Bid()
				# new_bid.contractor = Contractor.objects.get(id=request.session['contractor_id'])
				# new_bid.task = Task.objects.get(id=request.POST['task_id'])
				# new_bid.bid_type = request.POST['bid_type']
				# new_bid.amount = request.POST['amount']
				# new_bid.estimated_hours = request.POST['estimated_hours']
				# new_bid.save()

				# send object through redis channel 
				# bid = Bid.objects.get(id=new_bid.id)
				r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

				auction_id = request.POST['task_id']
				print auction_id
				channel = "auction"+str(auction_id)
				print channel

				context = BidSerializer(bid)
				context = context.data

				context = json.dumps(context)

				r.publish(channel, context)

				print("bid submitted")
				messages.success(request, "Your bid was successfully submitted")
				return HttpResponseRedirect('%s'%(reverse('tasks:task_detail', args=[pk])))
				# return HttpResponse("Everything worked")
		else:
			print("bid unsuccessful")
			# add a message
			messages.warning(request, "There was a problem with your bid. Please enter another one.")
			return HttpResponseRedirect('%s'%(reverse('tasks:task_detail', args=[pk])))


def accept_bid(request):
	
	if request.method == "POST":
		### need to clean data ###
    
		task_id = request.POST['task_id']
		bid_id = request.POST['bid_id']
		contractor_id = request.POST['contractor_id']

		task = Task.objects.get(id=task_id)
		bid = Bid.objects.get(id=bid_id)
		contractor = User.objects.get(id=contractor_id)

		task.contractor = contractor
		task.task_status = 'Active'
		task.bidding_closed_at = timezone.now()

		bid.is_accepted = True
		bid.accepted_at = timezone.now()
		bid.save()

		task.final_bid = bid
		task.save()

		print("bid accepted")

		"""
		once final_bid is set, start a chat with both parties
		"""

		return HttpResponseRedirect('%s'%(reverse('tasks:task_detail_active', args=[task_id])))
	else:
		messages.error(request, "Your bid could not be accepted. Please try again.")
		return HttpResponseRedirect('%s'%(reverse('tasks:task_detail', args=[task_id])))


class TaskMatchedView(DetailView):
	model = Task
	template_name = 'tasks/single_task_partials/active_task.html'

	def get_context_data(self, **kwargs):
		context = super(TaskMatchedView, self).get_context_data(**kwargs)
		user = self.object.user
		contractor = self.object.contractor
		context['user'] = user
		context['contractor'] = contractor
		return context

"""
Without the @csrf_exempt, we get a "Forbidden missin csrf_token" error
With the @csrf_exempt, we get a AttributeError => "'Task' object has no attribute 'get'", BUT
the task_clock_in time is registered in the admin side, BUT the button doesn't change colors

"""
@csrf_exempt
def start_task(request):
	if request.method == "POST":
		task = Task.objects.get(id=request.POST['task_id'])
		task.task_clock_in = timezone.localtime(timezone.now())
		task.save()
		messages.info(request, "Your task has been started.")
		return HttpResponseRedirect('%s'%(reverse('tasks:task_detail_active',args=[task.id])))

@csrf_exempt
def end_task(request):
	if request.method == "POST":
		user = request.user
		task = Task.objects.get(id=request.POST['task_id'])
		task.task_clock_out = timezone.localtime(timezone.now())
		# print(task.task_clock_out)
		print("=============")
		print(task.task_clock_out.hour)
		print("=============")
		task.save()

		# calculate the total_hours
		total_hours = task.task_clock_out.hour - task.task_clock_in.hour
		print(total_hours)
		print(task.final_bid.amount)
		# payment = total_hours * task.final_bid.amount
		if total_hours < 1:
			total_hours = 1

		task.final_payment = total_hours * task.final_bid.amount
		# payment = task.final_payment
		print(task.final_payment)
		task.task_status = "Completed"
		task.task_completed_at = timezone.localtime(timezone.now())
		task.is_completed = True
		task.save()

		messages.success(request, "Your task has been completed.")
		return HttpResponseRedirect('%s'%(reverse('tasks:task_detail_active',args=[task.id])))

def send_payment(request):
	if request.method == "POST":
		stripe.api_key = 'sk_test_BvXnJuHaPBDFDR0nou3Qq4Qn'

		task = Task.objects.get(id=request.POST['task_id'])
		payment = task.final_payment
		payment = payment*100
		payment = int(payment)
		print(payment)
		print("=======")
		print("the total payment is: " + str(payment))
		print("=======")
		client = request.user
		contractor = User.objects.get(id=request.POST['contractor_id'])
		
		# stripe_token = request.POST['stripeToken']

		client_account = stripe.Account.retrieve(client.stripe_account_id)
		client_customer_account = stripe.Customer.retrieve(client.stripe_customer_id)
		client_bank_account = client_account.external_accounts.retrieve(client.stripe_bank_account_id)
		print("===============")
		print("the client account is: " + client_account.id)
		print("===============")
		contractor_account = stripe.Account.retrieve(contractor.stripe_account_id)
		contractor_bank_account = contractor_account.external_accounts.retrieve(contractor.stripe_bank_account_id)
		print("===============")
		print("the contractor account is: " + contractor_account.id)
		print("===============")
		

		### calculate the application_fee ###


		# charge the client

		"""
		customer => who is going to be charged (i.e. passenger)
		destination => who is receiving the money (i.e. driver)
		"""

		result = stripe.Charge.create(
		  amount=payment,
		  currency='usd',
		  # source=stripe_token,
		  application_fee=1000,
		  customer=client_customer_account, 			# needs to be a cus_xxxxxxxx
		  destination=contractor_account, 	# needs to be the acct_xxxxxx of recipient
		)
		print("=============")
		print("payment sent: " + result.id)
		print("=============")

		if result.id:
			task.task_status = "Paid"
			task.save()
			messages.success(request, "Your payment has been sent.")
			return HttpResponseRedirect('%s'%(reverse('tasks:task_detail_active',args=[task.id])))
		else:
			messages.warning(request, "Something went wrong with payment")
			return HttpResponseRedirect('%s'%(reverse('tasks:task_detail_active',args=[task.id])))


		# result = braintree.Transaction.sale({
		# 	"amount": payment,
		# 	"payment_method_token": user.payment_method_token,
		# 	"customer_id": user.braintree_id,
		# 	"options": {
		# 		"submit_for_settlement": True
		# 	}
		# })
		# if result.is_success:
		# 	task.task_status = "Paid"
		# 	task.save()
		# 	messages.success(request, "Your payment has been sent.")
		# 	return HttpResponseRedirect('%s'%(reverse('tasks:task_detail_active',args=[task.id])))
		# else:
		# 	# messages.error(request, "Oops, something went wrong with your payment.")
		# 	messages.warning(request, '%s'%(result.message))
		# 	return HttpResponseRedirect('%s'%(reverse('tasks:task_detail_active',args=[task.id])))



"""
===============
ListView(s) for task partials in user dashboard
===============
"""
class AllTaskListView(ListView):
	model = Task
	template_name = "accounts/partials/users/partials/tasks/all.html"

	def get(self, request, *args, **kwargs):
		user = User.objects.get(id=request.session['user_id'])
		tasks = Task.objects.filter(user=user)
		context = {
			'tasks': tasks,
		}
		return render(request, self.template_name, context)

class ActiveTaskListView(ListView):
	model = Task
	template_name = "accounts/partials/users/partials/tasks/active.html"

	def get(self, request, *args, **kwargs):
		user = User.objects.get(id=request.session['user_id'])
		tasks = Task.objects.filter(user=user).filter(task_status="Active")
		context = {
			'tasks': tasks,
		}
		return render(request, self.template_name, context)

class OpenTaskListView(ListView):
	model = Task
	template_name = "accounts/partials/users/partials/tasks/open.html"
	
	def get(self, request, *args, **kwargs):
		user = User.objects.get(id=request.session['user_id'])
		tasks = Task.objects.filter(user=user).filter(task_status="Open")
		context = {
			'tasks': tasks,
		}
		return render(request, self.template_name, context)

class CompletedTaskListView(ListView):
	model = Task
	template_name = "accounts/partials/users/partials/tasks/completed.html"

	def get(self, request, *args, **kwargs):
		user = User.objects.get(id=request.session['user_id'])
		tasks = Task.objects.filter(user=user).filter(task_status="Paid")
		context = {
			'tasks': tasks,
		}
		return render(request, self.template_name, context)







