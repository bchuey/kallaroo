from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from .models import User, UserAddress
from ..categories.models import Subcategory
import re
"""
==============
Registration
==============
"""

class UserCreationForm(forms.ModelForm):
	username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'choose a username'}))
	email = forms.EmailField(label='Email', max_length=255, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter a valid email address'}))
	first_name = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'your first name'}))
	last_name = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'your last name'}))
	profile_pic = forms.ImageField(label='Profile Picture', widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
	password1 = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'create a password'}))
	password2 = forms.CharField(label='Confirm Password', max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'re-enter your password'}))
	is_contractor = forms.BooleanField(label='Are you a contractor?', required=False, widget=forms.CheckboxInput())
	subcategory = forms.ModelChoiceField(label='Subcategory', queryset=Subcategory.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), required=False)

	class Meta:
		model = User
		fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'profile_pic', 'is_contractor', 'subcategory')

	def clean_username(self):
		username = self.cleaned_data.get('username')
		
		try:
			user = User.objects.all().filter(username=username)
			if user:
				raise forms.ValidationError("Sorry, an account with that username has already been registered.")
		except:
			pass

		return username

	def clean_email(self):
		EMAIL_REGEX = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b')
		email = self.cleaned_data.get('email')
		
		try:
			user = User.objects.all().filter(email=email)
			if user:
				raise forms.ValidationError("Sorry, this email has already been registered.")
		except:
			pass

		if not EMAIL_REGEX.match(email):
			raise forms.ValidationError("Invalid email. Please try again.")
		return email

	def clean_first_name(self):
		NAME_REGEX = re.compile(r'\b[a-zA-Z]+$\b')
		first_name = self.cleaned_data.get('first_name')
		if not NAME_REGEX.match(first_name):
			raise forms.ValidationError("Invalid name. Your first name must only include letters.")
		return first_name

	def clean_last_name(self):
		NAME_REGEX = re.compile(r'\b[a-zA-Z]+$\b')
		last_name = self.cleaned_data.get('last_name')
		if not NAME_REGEX.match(last_name):
			raise forms.ValidationError("Invalid name. Your first name must only include letters.")
		return last_name


	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class FullUserAddressForm(forms.ModelForm):
	STATE_CHOICES = (
		('AZ', 'AZ'),
		('CA', 'CA'),
		('TX', 'TX'),
	)
	street_number = forms.IntegerField(label="Street Number", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Street Number e.g. 1121'}))
	street_address = forms.CharField(label="Street Address", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Street Address e.g. Mission St.'}))
	city = forms.CharField(label="City", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City e.g. San Francisco'}))
	state = forms.ChoiceField(label='State', choices=STATE_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
	postal_code = forms.IntegerField(label="Postal Code", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Postal Code e.g. 94011 or 94011-0922'}))

	class Meta:
		model = UserAddress
		fields = ('street_number', 'street_address', 'city', 'state', 'postal_code')

	def clean_street_number(self):
		street_number = self.cleaned_data.get('street_number')
		STREET_NUMBER_REGEX = re.compile(r'[0-9]+$')
		if not STREET_NUMBER_REGEX.match(street_number):
			raise forms.ValidationError("Street Number can only contain digits 0-9")
		return street_number


	def clean_street_address(self):
		street_address = self.cleaned_data.get('street_address')
		STREET_ADDRESS_REGEX = re.compile(r'[a-zA-Z\-]+')
		if not STREET_ADDRESS_REGEX.match(street_address):
			raise forms.ValidationError("Street Address can only contain lowercase/uppercase letters, and dashes.")
		return street_address


	def clean_city(self):
		city = self.cleaned_data.get('city')
		CITY_REGEX = re.compile(r'[a-zA-Z\-]+')
		if not CITY_REGEX.match(street_address):
			raise forms.ValidationError("Valid city names can only contain lowercase/uppercase letters, and dashes.")
		return city

	def clean_state(self):
		pass

	def clean_postal_code(self):
		postal_code = self.cleaned_data.get('postal_code')
		POSTAL_CODE_REGEX = re.compile(r'\d{5}(-\d{4})?$')
		# 99577-0727
		if not POSTAL_CODE_REGEX.match(postal_code):
			raise forms.ValidationError("Invalid postal code combination")
		return postal_code


class UserAddressForm(forms.ModelForm):
	address = forms.CharField(label='ADDRESS', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter your location'}))

	class Meta:
		model = User
		fields = ['address']

class UserChangeForm(forms.ModelForm):
	username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(label='Email', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control'}, render_value=True))

	class Meta:
		model = User
		fields = ('email', 'username', 'first_name', 'last_name', 'password')

	def clean_password(self):
		return self.initial['password']

"""
============
Stripe form 
============
"""

class StripePaymentForm(forms.Form):
	MONTH_CHOICES = (
		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('8', '8'),
		('9', '9'),
		('10', '10'),
		('11', '11'),
		('12', '12'),

	)
	date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type':'date','class':'form-control'}), input_formats=['%m/%d/%Y'])
	# cc_number = forms.CharField(label='Credit Card Number', widget=forms.TextInput(attrs={'class':'form-control','data-stripe':'number'}))
	# cc_cvc = forms.CharField(label='CVC', widget=forms.TextInput(attrs={'class':'form-control','data-stripe':'cvc'}))
	# exp_month = forms.ChoiceField(label='Exp Month', widget=forms.Select(attrs={'class':'form-control','data-stripe':'exp-month'}), choices=MONTH_CHOICES)
	# exp_year = forms.IntegerField(label='Exp Year', widget=forms.NumberInput(attrs={'class':'form-control','data-stripe':'exp-year'}))

	bank_account = forms.CharField(label='Bank Account #', max_length=255, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'please enter your bank account #'}))
	bank_name = forms.CharField(label='Bank Name', max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'please enter the name of your bank'}))
	routing_number = forms.CharField(label='Routing #', max_length=255, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'please enter your routing #'}))
	
	# clean the info somehow


"""
===============
Login
===============
"""


class LoginForm(forms.ModelForm):
	email = forms.EmailField(label='Email', max_length=255, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'please enter your email'}))
	password = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'please enter your password'}))

	class Meta:
		model = User
		fields = ('email', 'password')