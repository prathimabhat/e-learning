from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
#from student_management.models import Subjects
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class CustomUser(AbstractUser):
	username=None
	email=models.EmailField(_('email address'),unique=True)
	USERNAME_FIELD='email'
	REQUIRED_FIELDS=[]

	user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Student"), (4, "Parent"))
	user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
	objects=CustomUserManager() 

	def __str__(self):
		return f"{self.email}"

class SessionYearModel(models.Model):
	class Meta:
		verbose_name_plural="Session year"

	id = models.AutoField(primary_key=True)
	session_start_year = models.DateField()
	session_end_year = models.DateField()
	name=models.CharField(max_length=500,blank=True)
	objects=models.Manager()
	def __str__(self):
		return f"{self.name} -> {self.session_start_year} to {self.session_end_year}"


class AdminHOD(models.Model):
	class Meta:
		verbose_name_plural="Admin(HOD)"

	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True)
	admin_name=models.CharField(max_length=255)
	dob = models.DateField(null=True)
	blood_group = models.CharField(max_length=10,blank=True,null=True)
	qualification = models.CharField(max_length=50,blank=True,null=True)
	gender = models.CharField(max_length=255,blank=True,null=True)
	profile_pic = models.FileField(null=True)
	ph_no = models.CharField(max_length=10,blank=True,null=True)
	address = models.TextField(blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	objects = CustomUserManager()

	def __str__(self):
		return f"{self.id} {self.admin_name}"



class Staffs(models.Model):
	class Meta:
		verbose_name_plural="Staff"

	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True)
	staff_name=models.CharField(max_length=255)
	teacher_roll_number = models.CharField(max_length=50)
	dob = models.DateField(null=True)
	blood_group = models.CharField(max_length=10)
	qualification = models.CharField(max_length=50)
	gender = models.CharField(max_length=255)
	profile_pic = models.FileField()
	ph_no = models.CharField(max_length=10)
	address = models.TextField()
	# fcm_token = models.TextField(default="")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	objects = CustomUserManager()

	def __str__(self):
		return f"{self.id}"



class Courses(models.Model):
	id = models.AutoField(primary_key=True)
	course_name = models.CharField(max_length=255)
	session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE,related_name='course',null=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	objects = models.Manager()
	class Meta:
		ordering = ['session_year_id']

	def __str__(self):
		return f"{self.course_name}"

class Students(models.Model):
	class Meta:
		verbose_name_plural="Students"

	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True)
	student_name=models.CharField(max_length=255)
	gender = models.CharField(max_length=255)
	roll_number = models.CharField(max_length=50)
	blood_group = models.CharField(max_length=10)
	#parent_roll_number = models.ForeignKey(Parents, on_delete=models.CASCADE)
	profile_pic = models.FileField()
	ph_no = models.CharField(max_length=10)
	dob = models.DateField(null=True)
	# fcm_token = models.TextField(default="")
	address = models.TextField()
	#subject_id= models.ManyToManyField(Subjects,related_name="subject",null=True)
	course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING,null=True,blank=True)
	session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE,related_name='student',null=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	objects = CustomUserManager()


	def __str__(self):
		return f"{self.id}"
class Parents(models.Model):
	class Meta:
		verbose_name_plural="Parents"

	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True)
	parent_of=models.ForeignKey(Students,on_delete=models.CASCADE,null=True)
	father_name=models.CharField(max_length=255)
	father_occupation = models.CharField(max_length=255)
	#parent_roll_number=models.CharField(max_length=50)
	mother_name=models.CharField(max_length=255)
	mother_occupation = models.CharField(max_length=255)
	parent_ph_no = models.CharField(max_length=10)
	# fcm_token = models.TextField(default="")
	parent_address = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	objects = CustomUserManager()

	def __str__(self):
		return f"{self.id}"

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == '1':
            AdminHOD.objects.create(user=instance)
        if instance.user_type == '2':
            Staffs.objects.create(user=instance)
        if instance.user_type == '3':
            Students.objects.create(user=instance)
        if instance.user_type == '4':
            Parents.objects.create(user=instance)

from django.core.exceptions import ObjectDoesNotExist
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
	try:
	    if instance.user_type == '1':
	        instance.adminhod.save()
	    if instance.user_type == '2':
	        instance.staffs.save()
	    if instance.user_type == '3':
	        instance.students.save()
	    if instance.user_type == '4':
	        instance.parents.save()

	except ObjectDoesNotExist:
		if instance.user_type == '1':
			AdminHOD.objects.create(user=instance)
		if instance.user_type == '2':
			Staffs.objects.create(user=instance)
		if instance.user_type == '3':
			Students.objects.create(user=instance)
		if instance.user_type == '4':
			Parents.objects.create(user=instance)



   
