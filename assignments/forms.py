## @brief Forms for the course app.

from django import forms
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from .models import Message,Submission,LectureLinks,Quiz,QuizQuestions,QuizChoice
from student_management.models import Subjects

## @brief This class represents the form to send a message in the forum.
class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['content']


## @brief This class represents the form to add a submission for an assignment.
class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = ['file_submitted']

from .models import Assignment,Notification, Resources

## @brief This class represents the form to add a notification.
class NotificationForm(forms.ModelForm):

    class Meta:
        model = Notification
        fields = ['content']


## @brief This class represents the form to add an assignment.
class AssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False
        #self.fields['link'].required = False
        self.fields['text_assignment'].required = False

    description=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Type a description'}))
   
    text_assignment=forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control','placeholder': 'Type here'}))

    
    deadline = forms.DateTimeField( input_formats = ['%Y-%m-%dT%H:%M'],widget=forms.DateTimeInput(attrs={'type':'datetime-local','class': 'form-control'},
            format='%Y-%m-%dT%H:%M'))

    class Meta:
        model = Assignment
        fields = ['description', 'text_assignment','file', 'deadline','max_marks']


## @brief This class represents the form to add a resource.
class ResourceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        self.fields['file_resource'].required = False
        self.fields['link'].required = False
        self.fields['text_resource'].required = False
    text_resource=forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control','placeholder': 'Type here'}))
    title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}))
    link=forms.URLField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Paste links'}))
    class Meta:
        model = Resources
        fields = ['title', 'file_resource','link','text_resource']

class LecturelinksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(LecturelinksForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subjects.objects.filter(staff_id=user)

    subject = forms.ModelChoiceField(queryset=None, widget=forms.Select, required=True)
    link=forms.URLField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Paste links'}))
    description=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Type a description'}))
    #subject=forms.ModelChoiceField(queryset=Subjects.objects.filter(staff_id=f),widget=forms.ChoiceInput(attrs={'class':'form-control'}))
    class Meta:
        model=LectureLinks
        fields=['description','link','subject']

class QuizForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(QuizForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subjects.objects.filter(staff_id=user)
        self.fields['time_for_quiz'].required=False
        self.fields['min_marks'].required=False

    quiz_name=forms.CharField(label="Quiz name",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter a name for the quiz '}))
    quiz_date=forms.DateTimeField(label="Date and time of quiz", input_formats = ['%Y-%m-%dT%H:%M'],widget=forms.DateTimeInput(attrs={'type':'datetime-local','class': 'form-control'},
            format='%Y-%m-%dT%H:%M'))
    time_for_quiz=forms.DurationField(label="Duration of the quiz",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'HH:MM:SS'}))

    total_marks=forms.IntegerField(label="Total marks",widget=forms.NumberInput(attrs={'class':'form-control','min':'0'}))
    min_marks=forms.IntegerField(label="Minimum marks to pass",widget=forms.NumberInput(attrs={'class':'form-control','min':'0'}))
    subject=forms.ModelChoiceField(queryset=None, widget=forms.Select, required=True)

    class Meta:
        model=Quiz
        fields=['quiz_name','quiz_date','total_marks','min_marks','time_for_quiz']

class QuizQuestionsForm(forms.ModelForm):
    #question_type=forms.CharField(help_text="example:objective,subjective",label="Question type",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter type of question'}))
    question_text=forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control','placeholder': 'Type here'}))
    question_marks=forms.IntegerField(label="Total marks",widget=forms.NumberInput(attrs={'class':'form-control','min':'0'}))

    class Meta:
        model=QuizQuestions
        fields=['question_text','question_marks']

class MCQForm(forms.ModelForm):
    choice1=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    choice2=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    choice3=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    choice4=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        
        model=QuizChoice
        fields=['choice1','choice2','choice3','choice4']
