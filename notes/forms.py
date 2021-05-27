from django import forms
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from .models import notes
class NotesForm(forms.ModelForm):

	class Meta:
		model=notes
		fields=['name','file']

class WriteNotesForm(forms.ModelForm):
	name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','width':'15'}))
	note_text=forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control','placeholder':'Type here'}))
	class Meta:
		model=notes
		fields=['name','note_text']

class EditForm(forms.ModelForm):
	name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}))
	note_text=forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control','placeholder':'Type here'}))
	class Meta:
		model=notes
		fields=['name','note_text']