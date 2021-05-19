from django.shortcuts import render
from django.shortcuts import render,redirect
from accounts.models import Students
from student_management.models import Subjects
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import AnswerForm,QuestionForm
from forum.models import Questions,Answers
from django.urls import reverse
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
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
		answers=Answers.objects.filter(question=question_id)
		context={
			'question':question,
			'answers':answers,
			
		}
		return render(request,'forum/questions.html',context)


class AnswerView(LoginRequiredMixin,CreateView):

	model=Answers
	form_class=AnswerForm
	success_url='/'
	
	def form_valid(self,form):
		
		
		question_=get_object_or_404(Questions,pk=self.kwargs['pk'])
		subject_=get_object_or_404(Subjects,subject_name=question_.subject.subject_name)
		obj=form.save(commit=False)
		obj.user=self.request.user.students
		obj.subject=subject_
		obj.question=question_
		obj.save()
		subject='New message'
		from_email=settings.EMAIL_HOST_USER
		to_email=self.request.user.email
		text_content="Hi, somebody answered your question.Login to see!"
		html_content=get_template("forum/answered_email.html").render()
		msg= EmailMultiAlternatives(subject,text_content,from_email,[to_email])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

		return super().form_valid(form)
		#return self.render_to_response(self.get_context_data(form=form))
		



class NewQuestionView(LoginRequiredMixin,CreateView):
	
	model=Questions
	form_class=QuestionForm
	success_url='/forum/'
	
	def form_valid(self,form):
		
		subject_=get_object_or_404(Subjects,subject_name=self.kwargs['subjects'])
		obj=form.save(commit=False)
		obj.user=self.request.user.students
		obj.subject=subject_
		obj.save()
		return super().form_valid(form)
	

def QuestionUpVoteView(request,*args,**kwargs):
	question=get_object_or_404(Questions,id=request.POST.get('question_id_up'))
	question.up_votes.add(request.user.profile)
	return HttpResponseRedirect(reverse('forum:question-detail',args=[int(kwargs['pk'])]))

def QuestionDownVoteView(request,*args,**kwargs):
	question=get_object_or_404(Questions,id=request.POST.get('question_id_down'))
	question.down_votes.add(request.user.profile)
	return HttpResponseRedirect(reverse('forum:question-detail',args=[int(kwargs['pk'])]))


def AnswerUpVoteView(request,*args,**kwargs):
	answer=get_object_or_404(Answers,id=request.POST.get('answer_id_up'))
	answer.up_votes.add(request.user.profile)
	return HttpResponseRedirect(reverse('forum:question-detail',args=[int(kwargs['pk_alt'])]))

def AnswerDownVoteView(request,*args,**kwargs):
	answer=get_object_or_404(Answers,id=request.POST.get('answer_id_down'))
	answer.down_votes.add(request.user.profile)
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
	user=get_object_or_404(Students,id=request.user.students.id)
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
		

		return redirect('forum:question-detail',question.id)
	return render(request,"forum/report.html",context)

@login_required
def ReportAnswerView(request,*args,**kwargs):
	answer=get_object_or_404(Answers,id=kwargs['pk'])
	question=get_object_or_404(Questions,id=answer.question.id)
	admins=AdminHOD.objects.all()
	user=get_object_or_404(Students,id=request.user.profile.id)
	
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
		html_message = render_to_string('community_forum/answer_mail.html',ctx,request=request)
		plain_message = strip_tags(html_message)
		to_email=[]
		for i in admins:
			print(i.user.email)
			to_email.append(i.user.email)
			print(to_email)
		mail.send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
		return redirect('community_forum:question-detail',question.id)
	return render(request,"community_forum/report.html")
