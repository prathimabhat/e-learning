from django import forms
from django.forms import ModelForm
from .models import Answers,Questions
from ckeditor.widgets import CKEditorWidget
class AnswerForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(AnswerForm, self).__init__(*args, **kwargs)
		self.fields['anonymous'].required = False

	answer=forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control','placeholder': 'Type here'}))
	anonymous = forms.BooleanField()
	class Meta:
		model=Answers
		fields=['answer','anonymous']
		
   
class QuestionForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(QuestionForm, self).__init__(*args, **kwargs)
		self.fields['anonymous'].required = False


	question_title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Give a title to your question','size':'20'}))
	question_detail=forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control','placeholder': 'Type here'}))
	anonymous=forms.BooleanField()
	class Meta:
		model=Questions
		fields=['question_title','question_detail','anonymous']

class AnswerUpdateForm(forms.ModelForm):
	answer=forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control','placeholder':'Type here'}))
	class Meta:
		model=Answers
		fields=['answer']


class QuestionUpdateForm(forms.ModelForm):
	question_title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Give a title to your question'}))
	question_detail=forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control','placeholder':'Type here'}))
	class Meta:
		model=Questions
		fields=['question_title','question_detail']

class AnswerUpdateForm(forms.ModelForm):

	answer=forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control','placeholder':'Type here'}))
	class Meta:
		model=Answers
		fields=['answer']

