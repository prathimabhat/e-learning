from django import forms
from .models import CustomUser


class AuthenticationForm(forms.Form):
	email=forms.EmailField(label='Enter your email address',widget=forms.EmailInput(attrs={'placeholder': 'jondoe@example.com','size':'40'}))
	password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'placeholder':'password','size':'40'}))
	class Meta:
		model=CustomUser
		fields=['username','password']

