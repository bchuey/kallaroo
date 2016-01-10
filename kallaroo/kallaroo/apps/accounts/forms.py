from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from .models import User, UserAddress, Contractor, ContractorProfile
from ..categories.models import Subcategory


class LoginForm(forms.ModelForm):
	email = forms.EmailField(label='Email', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ('email', 'password')

class UserCreationForm(forms.ModelForm):
	username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(label='Email', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	profile_pic = forms.ImageField(label='Profile Picture', widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
	password1 = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label='Confirm Password', max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control'}))
	

	class Meta:
		model = User
		fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'profile_pic')

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

class ContractorRegisterForm(forms.ModelForm):
	username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(label='Email', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label='Confirm Password', max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control'}))
	subcategory = forms.ModelChoiceField(label='Subcategory', queryset=Subcategory.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
	profile_pic = forms.ImageField(label='Profile Picture', widget=forms.ClearableFileInput(attrs={'class':'form-control'}))

	class Meta:
		model = Contractor
		fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2', 'subcategory', 'profile_pic')

	def clean_confirm_password(self):
		new_password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password and password2 and password != password2:
			raise forms.ValidationError("Password do not match.")
		return password2

	def clean_email(self):
		email = self.cleaned_data.get("email")
		contractor_count = Contractor.objects.filter(email=email).count()
		if contractor_count > 0:
			raise forms.ValidationError("This email has already been registered. Please check and try again or reset your password.")
		return email

	def save(self, commit=True):
		contractor = super(ContractorRegisterForm, self).save(commit=False)
		contractor.password = self.cleaned_data['password']
		if commit:
			contractor.save()
		return contractor

class ContractorProfileForm(forms.ModelForm):
	description = forms.CharField(label='description', widget=forms.Textarea)

	class Meta:
		model = ContractorProfile
		fields = ['description']

class ContractorLoginForm(forms.Form):
	email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

	def clean_email(self):
		email = self.cleaned_data.get("email")
		try:
			contractor = Contractor.objects.get(email=email)
		except Contractor.DoesNotExist:
			raise forms.ValidationError("The email is not registered.")
		return email

	def clean_password(self):
		email = self.cleaned_data.get("email")
		password = self.cleaned_data.get("password")
		try:
			contractor = Contractor.objects.get(email=email)
		except:
			contractor = None
		# if contractor is not None and not contractor.check_password(password):
		if contractor is not None:
			if contractor.password != password:
				raise forms.ValidationError("Invalid password")
			elif contractor is None:
				pass
			else:
				return password
