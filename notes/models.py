from django.db import models
from accounts.models import Students
from ckeditor.fields import RichTextField
from student_management.models import Subjects
# Create your models here.
class notes(models.Model):
	class Meta:
		verbose_name_plural="Notes"

	id=models.AutoField(primary_key=True,unique=True)
	student=models.ForeignKey(Students,related_name="notes",on_delete=models.CASCADE,null=True)
	subject=models.ForeignKey(Subjects,related_name="notes",on_delete=models.CASCADE,null=True)
	name=models.CharField(max_length=200,blank=True,null=True)
	file=models.FileField(null=True)
	note_text=RichTextField(blank=True,null=True)
	post_time = models.DateTimeField(auto_now_add="True",null=True)
	last_edited=models.DateTimeField(auto_now_add="True",null=True)

	def __str__(self):
		return f"{self.id}"
