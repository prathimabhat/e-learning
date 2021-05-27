## @brief Forms for the course app.

from django import forms
from django.contrib.auth.models import User

from .models import Message,Submission


## @brief This class represents the form to send a message in the forum.
class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['content']


## @brief This class represents the form to add a submission for an assignment.
class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = ['file_submitted', 'feedback']

from .models import Assignment,Notification, Resources

## @brief This class represents the form to add a notification.
class NotificationForm(forms.ModelForm):

    class Meta:
        model = Notification
        fields = ['content']


## @brief This class represents the form to add an assignment.
class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ['description', 'file', 'deadline']


## @brief This class represents the form to add a resource.
class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resources
        fields = ['title', 'file_resource']