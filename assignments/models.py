from django.db import models
from accounts.models import Students
from student_management.models import Subjects
# Create your models here.
class Assignment(models.Model):
    ## The description of the assignment
    description = models.CharField(max_length=1000, default='')

    ## The file containing the problems for the assignment
    file = models.FileField(default='')

    ## The course associated with the assignment
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE,related_name='assignment')

    ## The date,time of posting the assignment
    post_time = models.CharField(max_length=100)

    ## The deadline to complete the assignment for the students
    deadline = models.CharField(max_length=100)


## @brief This class represents the submissions for an assignment.
class Submission(models.Model):
    ## The file submitted by student
    file_submitted = models.FileField(default='')

    ## The date,time of uploading the submission
    time_submitted = models.CharField(max_length=100)

    ## The user associated with the submission(who uploaded the submission)
    user = models.ForeignKey(Students, default=1,on_delete=models.CASCADE,related_name='submission')

    ## The assignment associated with the submission
    assignment = models.ForeignKey(Assignment, default=1,on_delete=models.CASCADE,related_name='submission')

    ## @var The list of integer choices available to give feedback for the assignment for which the submission is uploaded
    CHOICES = [(i+1, i+1) for i in range(10)]

    ## The feedback given to the assignment by the student while uploading the submission
    feedback = models.IntegerField(choices=CHOICES)