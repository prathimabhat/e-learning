from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
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
	objects=models.Manager()
	def __str__(self):
		return f"{self.session_start_year} to {self.session_end_year}"


class AdminHOD(models.Model):
	class Meta:
		verbose_name_plural="Admin(HOD)"

	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	admin_name=models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	objects = CustomUserManager()

	def __str__(self):
		return f"{self.id} {self.admin_name}"

class Parents(models.Model):
	class Meta:
		verbose_name_plural="Parents"

	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	father_name=models.CharField(max_length=255)
	father_occupation = models.CharField(max_length=255)
	#parent_roll_number=models.CharField(max_length=50)
	mother_name=models.CharField(max_length=255)
	mother_occupation = models.CharField(max_length=255)
	parent_ph_no = models.CharField(max_length=10)
	fcm_token = models.TextField(default="")
	parent_address = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	objects = CustomUserManager()

	def __str__(self):
		return f"{self.father_name}and {self.mother_name}"

class Staffs(models.Model):
	class Meta:
		verbose_name_plural="Staff"

	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	staff_name=models.CharField(max_length=255)
	teacher_roll_number = models.CharField(max_length=50)
	dob = models.DateField()
	blood_group = models.CharField(max_length=10)
	qualification = models.CharField(max_length=50)
	gender = models.CharField(max_length=255)
	profile_pic = models.FileField()
	ph_no = models.CharField(max_length=10)
	address = models.TextField()
	fcm_token = models.TextField(default="")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	objects = CustomUserManager()

	def __str__(self):
		return f"{self.staff_name}"



 

class Students(models.Model):
	class Meta:
		verbose_name_plural="Students"

	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='student')
	student_name=models.CharField(max_length=255)
	gender = models.CharField(max_length=255)
	roll_number = models.CharField(max_length=50)
	blood_group = models.CharField(max_length=10)
	#parent_roll_number = models.ForeignKey(Parents, on_delete=models.CASCADE)
	profile_pic = models.FileField()
	ph_no = models.CharField(max_length=10)
	dob = models.DateField()
	fcm_token = models.TextField(default="")
	address = models.TextField()
	#course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
	session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE,related_name='student')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	objects = CustomUserManager()


	def __str__(self):
		return f"{self.student_name}"


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(user=instance)
        if instance.user_type == 2:
            Staff.objects.create(user=instance)
        if instance.user_type == 3:
            Students.objects.create(user=instance)
        if instance.user_type == 4:
            Parents.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.students.save()
    if instance.user_type == 4:
        instance.parents.save()


   
