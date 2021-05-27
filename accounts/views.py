from django.shortcuts import render
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import transaction
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from accounts.backends import EmailBackEnd
from .forms import AuthenticationForm
# Create your views here.

def login_request(request):
    #print(request.user.user_type)
    if request.user.user_type=='1':
        return redirect('/admin_home')
    elif request.user.user_type=='2':
        return redirect('/staff_home')
    elif request.user.user_type=='3':
        return redirect('/student_home')
    elif request.user.user_type=='4':
        return redirect('/parent_home')
    else:
        return redirect('/accounts/login/')

        

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')