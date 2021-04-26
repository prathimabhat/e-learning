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

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.CustomUserManager()

class Parents(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    father_occupation = models.CharField(max_length=255)
    #parent_roll_number=models.CharField(max_length=50)
    mother_occupation = models.CharField(max_length=255)
    parent_ph_no = models.CharField(max_length=10)
    fcm_token = models.TextField(default="")
    parent_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.CustomUserManager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
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
    objects = models.CustomUserManager()