from django.shortcuts import render
from django.shortcuts import render,redirect
from accounts.models import Students,Staffs
from student_management.models import Subjects
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import AnswerForm,QuestionForm,\
QuestionUpdateForm,AnswerUpdateForm,StaffAnswerForm,\
StaffAnswerUpdateForm,TeacherQuestionForm
from forum.models import Questions,Answers
from django.urls import reverse
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.contrib import messages
import datetime
# Create your views here.



@login_required
def SubjectView(request, *args, **kwargs):

	subjects=Subjects.objects.filter(course_id=request.user.students.course_id).order_by('subject_name')
	context={
		'subjects':subjects
	}
	return render(request,'forum/SubjectView.html',context)

def SubforumView(request,*args,**kwargs):
	subject=kwargs['subject']
	subject_=get_object_or_404(Subjects,subject_name=subject)
	subject_questions=Questions.objects.filter(subject=subject_)

	return render(request,'forum/subforums.html',
			{'subject':subject,
			'subject_questions':subject_questions
			
			}
		)
class QuestionView(View):

	def get(self,request,*args,**kwargs):
		question_id=kwargs['pk']
		question=get_object_or_404(Questions,id=question_id)
		students=Students.objects.all()
		answers=Answers.objects.filter(question=question_id,user__in=students)

		context={
			'question':question,
			'answers':answers,
			
		}

		return render(request,'forum/questions.html',context)


		
def AnswerView(request,*args,**kwargs):
	form=AnswerForm
	if request.method=='POST':
		form=AnswerForm(request.POST)
		if form.is_valid():
			question_=get_object_or_404(Questions,pk=kwargs['pk'])
			subject_=get_object_or_404(Subjects,subject_name=question_.subject.subject_name)
			obj=form.save(commit=False)
			obj.user=request.user.students
			obj.subject=subject_
			obj.question=question_
			obj.date=datetime.datetime.now()
			obj.save()
			pk=kwargs['pk']

			
			return redirect('forum:question-detail',pk)
		else:
			form=AnswerForm()
	else:
		form=AnswerForm()
	context={
		'form':form,
	}
		
	return render(request,'forum/answers_form.html',context)	




@login_required
def NewQuestionView(request,*args,**kwargs):
	form=QuestionForm
	if request.method=='POST':
		form=QuestionForm(request.POST)
		if form.is_valid():
	
			
			subject_=get_object_or_404(Subjects,subject_name=kwargs['subjects'])
			obj=form.save(commit=False)
			obj.user=request.user.students
			obj.subject=subject_
			obj.date=datetime.datetime.now()	
			staff_id=subject_.staff_id.id
			teacher_=get_object_or_404(Staffs,id=staff_id)
			obj.teacher=teacher_
			obj.save()
			return redirect('forum:my_questions')
		else:
			form=QuestionForm()
	else:
		form=QuestionForm()
	context={
		'form':form,
	}
		
	return render(request,'forum/questions_form.html',context)

def QuestionUpVoteView(request,*args,**kwargs):
	question=get_object_or_404(Questions,id=request.POST.get('question_id_up'))
	question.up_votes.add(request.user.students)
	return HttpResponseRedirect(reverse('forum:question-detail',args=[int(kwargs['pk'])]))

def QuestionDownVoteView(request,*args,**kwargs):
	question=get_object_or_404(Questions,id=request.POST.get('question_id_down'))
	question.down_votes.add(request.user.students)
	return HttpResponseRedirect(reverse('forum:question-detail',args=[int(kwargs['pk'])]))


def AnswerUpVoteView(request,*args,**kwargs):
	answer=get_object_or_404(Answers,id=request.POST.get('answer_id_up'))

	answer.up_votes.add(request.user.students)
	return HttpResponseRedirect(reverse('forum:question-detail',args=[int(kwargs['pk_alt'])]))

def AnswerDownVoteView(request,*args,**kwargs):
	answer=get_object_or_404(Answers,id=request.POST.get('answer_id_down'))
	answer.down_votes.add(request.user.students)
	return HttpResponseRedirect(reverse('forum:question-detail',args=[int(kwargs['pk_alt'])]))

from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from accounts.models import AdminHOD

@login_required
def ReportView(request,*args,**kwargs):
	question=get_object_or_404(Questions,id=kwargs['pk'])
	admins=AdminHOD.objects.all()
	if(request.user.user_type =='3'):
		user=get_object_or_404(Students,id=request.user.students.id)
	if(request.user.user_type == '2'):
		user=get_object_or_404(Staffs,id=request.user.staffs.id)
	context = {
		'question': question
	}
	if request.method=='POST':

		qtn_type=request.POST.get('reason')
		
		ctx ={
			'user': user,
			'question': question,
			'qtn_type':qtn_type,
		}
		subject = "report"
		
		from_email = settings.EMAIL_HOST_USER
		html_message = render_to_string('forum/question_mail.html',ctx,request=request)
		plain_message = strip_tags(html_message)
		to_email=[]
		for i in admins:
			print(i.user.email)
			to_email.append(i.user.email)
			print(to_email)
		mail.send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
		
		messages.error(request, "Question reported!")
		if(request.user.user_type == '3'):
			return redirect('forum:question-detail',question.id)
		if(request.user.user_type == '2'):
			return redirect('forum:staff_question_detail',question.id)
	if(request.user.user_type == '3'):
		return render(request,"forum/report.html",context)
	if(request.user.user_type == '2'):
		return render(request,"staff_forum/report.html",context)

@login_required
def ReportAnswerView(request,*args,**kwargs):
	answer=get_object_or_404(Answers,id=kwargs['pk'])
	question=get_object_or_404(Questions,id=answer.question.id)
	admins=AdminHOD.objects.all()
	user=get_object_or_404(Students,id=request.user.students.id)
	
	if request.method=='POST':

		ans_type=request.POST.get('reason')
		
		ctx ={
			'user': user,
			'question': question,
			'ans_type':ans_type,
			'answer':answer
		}
		subject = "Report"
		from_email = settings.EMAIL_HOST_USER
		html_message = render_to_string('forum/answer_mail.html',ctx,request=request)
		plain_message = strip_tags(html_message)
		to_email=[]
		for i in admins:
			print(i.user.email)
			to_email.append(i.user.email)
			print(to_email)
		mail.send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
		messages.error(request, "Answer reported!")
		return redirect('forum:question-detail',question.id)
	return render(request,"forum/report.html")


class MyQuestionsView(LoginRequiredMixin,View):
	def get(self,request,*args,**kwargs):
		questions=Questions.objects.filter(user=self.request.user.students)
		context={
			'questions':questions
		}
		return render(request,'forum/my_questions.html',context)

class MyAnswersView(LoginRequiredMixin,View):
	def get(self,request,*args,**kwargs):

		answers=Answers.objects.filter(user=self.request.user.students)
		#questions=Questions.objects.filter(id=question_id)
		context={
			'answers':answers
		}
		return render(request,'forum/my_answers.html',context)


@login_required
def QuestionUpdateView(request,*args,**kwargs):
	context={}
	question_id=kwargs['pk']
	obj=get_object_or_404(Questions,id=question_id)
	form=QuestionUpdateForm(request.POST or None,instance=obj)
	if form.is_valid():
		form.save()
		#redirect_url=reverse('therapist_dashboard:AnswerView',args=[question_id])
		return redirect('/forum/my_questions/')
	context["form"]=form
	return render(request,'forum/question_update.html',context)

@login_required
def AnswerUpdateView(request,*args,**kwargs):
	context={}
	answer_id=kwargs['pk']
	obj=get_object_or_404(Answers,id=answer_id)
	form=AnswerUpdateForm(request.POST or None,instance=obj)
	if form.is_valid():
		form.save()
		#redirect_url=reverse('therapist_dashboard:AnswerView',args=[question_id])
		return redirect('/forum/my_answers/')
	context["form"]=form
	return render(request,'forum/answer_update.html',context)

@login_required
def QuestionDeleteView(request,pk):
	obj=get_object_or_404(Questions,id=pk)
	if request.method=='POST':
		obj.delete()
		return redirect('/forum/my_questions/')
	return render(request,'forum/delete_question.html')

def AnswerDeleteView(request,pk):
	
	obj=get_object_or_404(Answers,id=pk)
	question_id=obj.question.id
	if(request.user.user_type == '3'):
		if request.method=='POST':
			obj.delete()

			return redirect('/forum/my_answers/')
		return render(request,'forum/delete_answer.html')
	if(request.user.user_type == '2'):
		if request.method=='POST':
			
			obj.delete()

			return redirect('forum:staff_question_detail',question_id)
		return render(request,'staff_forum/delete_answer.html')



@login_required
def StaffSubjectView(request, *args, **kwargs):

	subjects=Subjects.objects.filter(staff_id=request.user.staffs.id).order_by('subject_name')
	context={
		'subjects':subjects
	}
	return render(request,'staff_forum/StaffSubjectView.html',context)

def StaffSubforumView(request,*args,**kwargs):
	subject=kwargs['subject']
	subject_=get_object_or_404(Subjects,subject_name=subject)
	subject_questions=Questions.objects.filter(subject=subject_,teachers_forum=True)

	return render(request,'staff_forum/Staffsubforum.html',
			{'subject':subject,
			'subject_questions':subject_questions
			
			}
		)

class StaffQuestionView(View):

	def get(self,request,*args,**kwargs):
		question_id=kwargs['pk']
		question=get_object_or_404(Questions,id=question_id)
		answers=Answers.objects.filter(question=question,teacher=request.user.staffs)

		context={
			'question':question,
			'answers':answers
			
			
		}

		return render(request,'staff_forum/staff_questions.html',context)

def StaffAnswerView(request,*args,**kwargs):
	form=AnswerForm
	if request.method=='POST':
		form=StaffAnswerForm(request.POST)
		if form.is_valid():
			question_=get_object_or_404(Questions,pk=kwargs['pk'])
			subject_=get_object_or_404(Subjects,subject_name=question_.subject.subject_name)
			obj=form.save(commit=False)
			obj.teacher=request.user.staffs
			obj.subject=subject_
			obj.question=question_
			obj.date=datetime.datetime.now()
			obj.save()
			pk=kwargs['pk']

			
			return redirect('forum:staff_question_detail',pk)
		else:
			form=StaffAnswerForm()
	else:
		form=StaffAnswerForm()
	context={
		'form':form,
	}
		
	return render(request,'staff_forum/staff_answers_form.html',context)

@login_required
def StaffAnswerUpdateView(request,*args,**kwargs):
	context={}
	answer_id=kwargs['pk']
	obj=get_object_or_404(Answers,id=answer_id)
	question_id=obj.question.id
	form=StaffAnswerUpdateForm(request.POST or None,instance=obj)
	if form.is_valid():
		form.save()
		#redirect_url=reverse('therapist_dashboard:AnswerView',args=[question_id])
		return redirect('forum:staff_question_detail',question_id)
	context["form"]=form
	return render(request,'staff_forum/staff_answer_update.html',context)

@login_required
def teacher_forum(request,*args,**kwargs):
	subjects=Subjects.objects.filter(course_id=request.user.students.course_id).order_by('subject_name')
	context={
		'subjects':subjects
	}
	return render(request,'forum/teacher_forum.html',context)

@login_required
def teacher_forum_questions(request,*args,**kwargs):
	sub=kwargs['pk']
	subject=get_object_or_404(Subjects,id=sub)
	staff_=get_object_or_404(Staffs,id=subject.staff_id.id)
	questions=Questions.objects.filter(user=request.user.students,teacher=staff_).order_by('-date')
	answers=Answers.objects.filter(question__in=questions,teacher=staff_).order_by('-date')
	context={
		'questions':questions,
		'answers':answers,
		'staff':staff_,
		'subject':subject
	}
	return render(request,'forum/teacher_forum_questions.html',context)
	
@login_required
def teacher_forum_new_question(request,*args,**kwargs):
	form=TeacherQuestionForm
	if request.method=='POST':
		form=TeacherQuestionForm(request.POST)
		if form.is_valid():
	
			
			subject_=get_object_or_404(Subjects,id=kwargs['pk'])
			obj=form.save(commit=False)
			obj.user=request.user.students
			obj.subject=subject_
			obj.date=datetime.datetime.now()	
			staff_id=subject_.staff_id.id
			teacher_=get_object_or_404(Staffs,id=staff_id)
			obj.teacher=teacher_
			obj.teachers_forum=True
			obj.save()
			pk=kwargs['pk']
			return redirect('forum:teacher_forum_questions',pk)
		else:
			form=TeacherQuestionForm()
	else:
		form=TeacherQuestionForm()
	context={
		'form':form,
	}
		
	return render(request,'forum/teacher_forum_questions_form.html',context)

