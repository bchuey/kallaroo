from django import forms
from . models import Review, Rating

RATING_CHOICES = (

	('1', '1'),
	('2', '2'),
	('3', '3'),
	('4', '4'),
	('5', '5'),

)
class CreateReviewForm(forms.ModelForm):
	comment = forms.CharField(label='Review', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Tell us about your experience...'}))
	rating = forms.ChoiceField(label='Rating', widget=forms.Select(attrs={'class':'form-control'}), choices=RATING_CHOICES)

	class Meta:
		model = Review
		fields = ('comment', 'rating',)

class CreateRatingForm(forms.ModelForm):
	value = forms.ChoiceField(label='Rating', widget=forms.Select(attrs={'class':'form-control'}), choices=RATING_CHOICES)

	class Meta:
		model = Rating
		fields = ('value',)


