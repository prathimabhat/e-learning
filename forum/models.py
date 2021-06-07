from django.db import models
from accounts.models import Students,Staffs
from student_management.models import Subjects
from ckeditor.fields import RichTextField
# Create your models here.
class Questions(models.Model):
	class Meta:
		verbose_name_plural="Questions"

	id=models.AutoField(primary_key=True,unique=True)
	user=models.ForeignKey(Students,on_delete=models.CASCADE,related_name='questions',blank=True,null=True)
	subject=models.ForeignKey(Subjects,on_delete=models.CASCADE,related_name='questions',blank=True,null=True)
	teacher=models.ForeignKey(Staffs,on_delete=models.CASCADE,related_name='questions',blank=True,null=True)
	question_title=models.CharField(max_length=300,blank=True,null=True)
	question_detail=RichTextField(blank=True,null=True)
	up_votes=models.ManyToManyField(Students,related_name='questions_up_votes')
	down_votes=models.ManyToManyField(Students,related_name='questions_down_votes')
	date=models.DateTimeField(auto_now_add=True)
	anonymous=models.BooleanField(default=False)
	teachers_forum=models.BooleanField(default=False)
	def __str__(self):
		return f"{self.question_title}"

	def total_upvotes(self):
		return self.up_votes.count()
	def total_downvotes(self):
		return self.down_votes.count()

class Answers(models.Model):
	class Meta:
		verbose_name_plural="Answers"

	id=models.AutoField(primary_key=True,unique=True)
	user=models.ForeignKey(Students,on_delete=models.CASCADE,related_name='answers',blank=True,null=True)
	subject=models.ForeignKey(Subjects,on_delete=models.CASCADE,related_name='answers',blank=True,null=True)
	teacher=models.ForeignKey(Staffs,on_delete=models.CASCADE,related_name='answers',blank=True,null=True)
	question=models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='answers',blank=True,null=True)
	answer=RichTextField(blank=True,null=True)
	up_votes=models.ManyToManyField(Students,related_name='answers_up_votes')
	down_votes=models.ManyToManyField(Students,related_name='answers_down_votes')
	date=models.DateTimeField(auto_now_add=True)
	anonymous = models.BooleanField(default=False)
	teachers_forum=models.BooleanField(default=False)

	def __str__(self):
		return f"{self.id}"

	def total_upvotes(self):
		return self.up_votes.count()
	def total_downvotes(self):
		return self.down_votes.count()