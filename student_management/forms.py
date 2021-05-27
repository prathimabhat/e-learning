'''from django import forms
from django.forms import ModelForm
from accounts.models import Staffs, Students,Parents
class newstaff(forms.ModelForm):
	staff_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter staff name'}))
	teacher_roll_number=forms.CharField(widget=forms.TextInput(attrs={'class':'form-cont
'''