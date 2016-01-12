from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, UserChangeForm, LoginForm, UserAddressForm
from .models import User, UserAddress
from ..categories.models import Subcategory
from ..tasks.models import Task
from ..tasks.forms import CreateTaskForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from formtools.wizard.views import NamedUrlSessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib import messages
import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
    merchant_id=settings.BRAINTREE_MERCHANT_ID,
    public_key=settings.BRAINTREE_PUBLIC,
    private_key=settings.BRAINTREE_PRIVATE,
)


class RegisterProfileView(View):
	model = User
	form = UserCreationForm
	template_name = 'accounts/register_user/step1.html'

	def get(self, request, *args, **kwargs):
		
		form = self.form()

		context = {
			'form': form,
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):

		form = UserCreationForm(request.POST, request.FILES)

		context = {
			'form': form,
		}

		
		if request.method == "POST":
			if form.is_valid():

				username = request.POST['username']
				email = request.POST['email']
				first_name = request.POST['first_name']
				last_name = request.POST['last_name']
				password = form.cleaned_data.get('password1')

				user = User.objects.create_user(email, username, first_name, last_name, password)
				user.profile_pic = request.FILES['profile_pic']
				
				try:
					user.is_contractor = request.POST['is_contractor']
					user.subcategory = request.POST['subcategory']
				except:
					pass

				user.braintree_id = user.get_braintree_id()

				user.braintree_client_token = user.get_client_token()

				user.save()

				user = authenticate(username=email, password=password)
				print(user)
				login(request, user)
				print("=============")
				print("user logged in")
				print("=============")
				request.session['user_id'] = user.id

				return HttpResponseRedirect('%s'%(reverse('accounts:register_address')))
			else:
				print("uh oh, something went wrong")
				return render(request, self.template_name, context)

class RegisterAddressView(View):
	model = UserAddress
	form = UserAddressForm
	template_name = 'accounts/register_user/step2.html'

	def get(self, request, *args, **kwargs):
		
		form = self.form()

		context = {
			'form': form,
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):

		form = UserAddressForm(request.POST)
		if request.method == "POST":
			if form.is_valid():
				# street_number = request.POST['street_number']
				# street_address = request.POST['street_address']
				# city = request.POST['city']
				# state = request.POST['state']
				# zipcode = request.POST['zipcode']

				# address = UserAddress.objects.create_address(street_number=street_number, street_address=street_address, city=city, state=state, zipcode=zipcode)

				# user = User.objects.get(id=request.session['user_id'])
				# address.user = user
				user = User.objects.get(id=request.session['user_id'])
				user.address = request.POST['address']
				# address.save()
				user.save()

				return HttpResponseRedirect('%s'%(reverse('accounts:register_payment')))
			else:
				return render(request, self.template_name, context)

class RegisterPaymentView(View):
	model = User
	template_name = 'accounts/register_user/step3.html'

	def get(self, request, *args, **kwargs):
		
		user = User.objects.get(id=request.session['user_id'])
		braintree_client_token = user.braintree_client_token
		context = {
			'braintree_client_token': braintree_client_token,
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		# print(request.POST.get('payment_method_nonce'))
		user = User.objects.get(id=request.session['user_id'])
		user.payment_method_nonce = request.POST.get('payment_method_nonce')
		user.save()

		result = braintree.PaymentMethod.create({
			"customer_id": user.braintree_id,
			"payment_method_nonce": user.payment_method_nonce,
		})

		if result.is_success:
			print("=============")
			print("success")
			print("=============")
			# print(result.payment_method)
			# print(result.payment_method.unique_number_identifier)
			# print(result.payment_method.token)
			user.payment_method_token = result.payment_method.token
			user.save()
			messages.success(request, "You have successfully registered your account.")

			return HttpResponseRedirect('%s'%(reverse('accounts:dashboard',args=[user.id])))
		else:
			print("=============")
			print("failed")
			print("=============")
			return HttpResponseRedirect('%s'%(reverse('accounts:register_payment')))

class UserProfileDetailView(DetailView):
	model = User
	template_name = 'accounts/partials/users/profile.html'
	form = UserChangeForm

	def get_context_data(self, **kwargs):
		context = super(UserProfileDetailView, self).get_context_data(**kwargs)
		user = self.object
		context['form'] = self.form(instance=user)
		return context

	def post(self, request, *args, **kwargs):
		pass

class UserTaskView(View):
	# model = User
	template_name = 'accounts/partials/users/tasks.html'
	form = CreateTaskForm

	def get(self, request, *args, **kwargs):
		# context = super(UserTaskView ,self).get_context_data(**kwargs)
		user = User.objects.get(id=request.session['user_id'])
		# context['form'] = self.form()
		# context['tasks'] = Task.objects.filter(user=user)
		tasks = Task.objects.filter(user=user)
		form = self.form()
		context = {

			'user': user,
			'tasks': tasks,
			'form': form,
		}
		return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class DashboardTemplateView(TemplateView):
	template_name = 'accounts/dashboard.html'

	def get_context_data(self, **kwargs):
		context = super(DashboardTemplateView, self).get_context_data(**kwargs)
		context['user'] = User.objects.get(id=self.request.session['user_id'])
		return context

class UsersListView(ListView):
	model = User
	template_name = 'accounts/user_list.html'

class AccountView(TemplateView):
	template_name = 'accounts/index.html'

	def get_context_data(self, **kwargs):
		context = super(AccountView, self).get_context_data(**kwargs)

		context['login_form'] = LoginForm
		return context


"""
Need to update the LoginUserView
"""

def login_user(request):
	context = {
		'register_form': UserCreationForm,
		'login_form': LoginForm,
	}

	form = LoginForm(request.POST)
	if request.method == "POST":
		"""
		AuthenticationForm uses id_username;
		username is dependent on USERNAME_FIELD in models;

		If you use custom LoginForm with id_email, set authenticate(username=email) (???)
		"""
		email = request.POST['email']
		password = request.POST['password']

		user = authenticate(username=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				print("=============")
				print("user logged in successfully")
				print(user)
				print("=============")
				request.session['user_id'] = user.id
				print("sessionid is: ")
				
				print(request.session.session_key)
				# return HttpResponseRedirect('/accounts/success')
				return HttpResponseRedirect('%s'%(reverse('accounts:dashboard',args=[request.session['user_id']])))
			else:
				return render(request, 'accounts/index.html', context)
		else:
			return render(request, 'accounts/index.html', context)
	else:
		return render(request, 'accounts/index.html', context)

def logout_view(request):
	logout(request)
	print("=============")
	print("user logged out successfully")
	print("=============")
	return HttpResponseRedirect('/accounts')

class SuccessView(TemplateView):
	template_name = 'accounts/success.html'



"""
=================
Contractor
=================
"""

class AllContractorsView(View):
	model = User
	template_name = 'accounts/contractors/all.html'

	def get(self, request, *args, **kwargs):
		contractors = User.objects.all().filter(is_contractor=True)
		context = {
			'contractors': contractors,
		}

		return render(request, self.template_name, context)

class ContractorProfileView(DetailView):
	model = User
	template_name = 'accounts/contractors/detail.html'






