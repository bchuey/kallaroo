from django import forms
from .models import Task, Bid
from ..categories.models import Subcategory

class ChooseSubcategoryForm(forms.ModelForm):
	subcategory = forms.ModelChoiceField(label='SUBCATEGORY', queryset=Subcategory.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))

	class Meta:
		model = Task
		fields = ['subcategory']

class SetAddressForm(forms.ModelForm):
	address = forms.CharField(label='ADDRESS', widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = Task
		fields = ['address']

class AddTaskDetailsForm(forms.ModelForm):
	title = forms.CharField(label='TITLE', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'give a short, but descriptive title'}))
	description = forms.CharField(label='DESCRIPTION', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'provide as much detail as you think the contractor will need...'}))
	special_instructions = forms.CharField(label='SPECIAL INSTRUCTIONS', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'anything else you might want to add?'}))

	class Meta:
		model = Task
		fields = ['title', 'description', 'special_instructions']

class CreateTaskForm(forms.ModelForm):

	STATE_CHOICES = (
		('AZ', 'AZ'),
		('CA', 'CA'),
		('TX', 'TX'),
	)

	title = forms.CharField(label='TITLE', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'give a short, but descriptive title'}))
	description = forms.CharField(label='DESCRIPTION', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'provide as much detail as you think the contractor will need...'}))
	special_instructions = forms.CharField(label='SPECIAL INSTRUCTIONS', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'anything else you might want to add?'}))
	subcategory = forms.ModelChoiceField(label='SUBCATEGORY', queryset=Subcategory.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
	

	# street_number = forms.IntegerField(label='STREET NUMBER', widget=forms.NumberInput(attrs={'class':'form-control'}))
	# street_address = forms.CharField(label='STREET ADDRESS', widget=forms.TextInput(attrs={'class':'form-control'}))
	# city = forms.CharField(label='CITY', widget=forms.TextInput(attrs={'class':'form-control'}))
	# state = forms.ChoiceField(label='STATE', choices=STATE_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
	# zipcode = forms.IntegerField(label='POSTAL CODE', widget=forms.NumberInput(attrs={'class':'form-control'}))

	address = forms.CharField(label='ADDRESS', widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = Task
		fields = ['title', 'description', 'special_instructions', 'subcategory', 'address']


class CreateBidForm(forms.ModelForm):
	BID_CHOICES = (

		('Hourly', 'Hourly'),
		('Project', 'Project'),

	)
	bid_type = forms.ChoiceField(choices=BID_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
	amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
	estimated_hours = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))

	class Meta:
		model = Bid
		fields = ['bid_type', 'amount', 'estimated_hours']
