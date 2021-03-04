from django import forms
from django.contrib.auth.forms import UserCreationForm

from .choices import NEWS_CATEGORY
from .models import UserExtended



class CustomUserForm(UserCreationForm):

	class Meta:
		model = UserExtended
		fields = ['username','email','password1','password2']
	
	def clean_email(self):
		email = self.cleaned_data.get('email')
		if UserExtended.objects.filter(email=email).exists():
			raise forms.ValidationError('This email is already in use.')
		return email


class UserLoginForm(forms.Form):

	email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class UserNewsCategory(forms.Form):

    user_news_choice = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=NEWS_CATEGORY)