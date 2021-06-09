from django.db import models
from accounts.models import Students,CustomUser
from student_management.models import Subjects
from ckeditor.fields import RichTextField
from django.utils import timezone
# Create your models here.
class Assignment(models.Model):
    ## The description of the assignment
    description = models.CharField(max_length=1000, default='')

    max_marks= models.PositiveIntegerField(null=True)

    text_assignment=RichTextField(blank=True,null=True)
    ## The file containing the problems for the assignment
    file = models.FileField(default='')

    ## The course associated with the assignment
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE,related_name='assignment',null=True)

    ## The date,time of posting the assignment
    post_time = models.DateTimeField(auto_now_add=True)

    ## The deadline to complete the assignment for the students
    deadline = models.DateTimeField(default=timezone.now)



## @brief This class represents the submissions for an assignment.
class Submission(models.Model):
    ## The file submitted by student
    file_submitted = models.FileField(default='')

    marks = models.PositiveIntegerField(null=True)

    ## The date,time of uploading the submission
    time_submitted = models.CharField(max_length=100)

    ## The user associated with the submission(who uploaded the submission)
    user = models.ForeignKey(Students, default=1,on_delete=models.CASCADE,related_name='submission')

    ## The assignment associated with the submission
    assignment = models.ForeignKey(Assignment, default=1,on_delete=models.CASCADE,related_name='submission')

    ## @var The list of integer choices available to give feedback for the assignment for which the submission is uploaded
    CHOICES = [(i+1, i+1) for i in range(10)]

    ## The feedback given to the assignment by the student while uploading the submission
    feedback = models.IntegerField(choices=CHOICES,null=True)


## @brief This class represents the messages displayed in the forum.
class Message(models.Model):
    ## The content of message
    content = models.CharField(max_length=500)

    ## The course associated with the message
    subject = models.ForeignKey(Subjects,default=1,on_delete=models.CASCADE,related_name='message')

    ## The sender of the message
    sender = models.ForeignKey(CustomUser,default=1, on_delete=models.CASCADE,related_name='sender')

    ## The time when the message was posted
    time = models.CharField(max_length=100)


## @brief This class represents the notifications receieved by the students.
class Notification(models.Model):
    ## The content of notification
    content = models.CharField(max_length=500)

    ## The course associated with the notification
    subject = models.ForeignKey(Subjects, default=1, on_delete=models.CASCADE,related_name="notification")

    ## The time when the notification was posted/generated
    time = models.CharField(max_length=100)


## @brief This class represents the resources(lectures/study materials) for a course.
class Resources(models.Model):
    ## The resource file 
    file_resource = models.FileField(default='')
    text_resource=RichTextField(blank=True,null=True)

    link=models.URLField(max_length=300,blank=True)
    ## The title for the resource
    title = models.CharField(max_length=100)

    ## The course associated with the resource
    subject = models.ForeignKey(Subjects, default=1, on_delete=models.CASCADE,related_name="resources")

    def __str__(self):
        return f"{self.id} ->{self.title}"

class LectureLinks(models.Model):
    link=models.URLField(max_length=300,blank=True)
    description=models.CharField(max_length=1000)
    subject = models.ForeignKey(Subjects, default=1, on_delete=models.CASCADE,related_name="lecturelinks")

    def __str__(self):
        return f"{self.id} -> {self.description}"