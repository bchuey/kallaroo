from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from .models import User, UserAddress
from ..categories.models import Subcategory

"""
==============
Registration
==============
"""

class UserCreationForm(forms.ModelForm):
	username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(label='Email', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	profile_pic = forms.ImageField(label='Profile Picture', widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
	password1 = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label='Confirm Password', max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control'}))
	is_contractor = forms.BooleanField(label='Are you a contrator?', required=False, widget=forms.CheckboxInput())
	subcategory = forms.ModelChoiceField(label='Subcategory', queryset=Subcategory.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'profile_pic', 'is_contractor', 'subcategory')

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

class UserAddressForm(forms.ModelForm):
	STATE_CHOICES = (
		('AZ', 'AZ'),
		('CA', 'CA'),
		('TX', 'TX'),
	)
	street_number = forms.IntegerField(label="Street Number", widget=forms.NumberInput(attrs={'class':'form-control'}))
	street_address = forms.CharField(label="Street Address", widget=forms.TextInput(attrs={'class':'form-control'}))
	city = forms.CharField(label="City", widget=forms.TextInput(attrs={'class':'form-control'}))
	state = forms.ChoiceField(label='State', choices=STATE_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
	zipcode = forms.IntegerField(label="Postal Code", widget=forms.NumberInput(attrs={'class':'form-control'}))

	class Meta:
		model = UserAddress
		fields = ('street_number', 'street_address', 'city', 'state', 'zipcode')

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
===============
Login
===============
"""


class LoginForm(forms.ModelForm):
	email = forms.EmailField(label='Email', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ('email', 'password')