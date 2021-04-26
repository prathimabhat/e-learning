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