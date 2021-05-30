from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from accounts.models import Students
from student_management.models import Subjects
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import notes
from .forms import NotesForm,WriteNotesForm,EditForm
import datetime
# Create your views here.

@login_required
def home(request):
	subjects=Subjects.objects.filter(course_id=request.user.students.course_id.id)
	context={
		'subjects':subjects
	}
	return render(request,'notes/home.html',context)

@login_required
def detail(request,*args,**kwargs):
	sub=kwargs['subject']
	subject=get_object_or_404(Subjects,id=sub)
	notes_=notes.objects.filter(subject=subject)
	context={
		'subject':subject,
		'notes':notes_
	}
	return render(request,'notes/detail.html',context)


@login_required
def upload_notes(request,*args,**kwargs):
	form=NotesForm()
	sub=kwargs['subject']
	if request.method=='POST':
		form=NotesForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			
			notes=form.save(commit="False")
			notes.file = request.FILES['file']
			notes.name=request.POST['name']
			notes.post_time = datetime.datetime.now()
			notes.student=get_object_or_404(Students,id=request.user.students.id)
			notes.subject=get_object_or_404(Subjects,id=sub)
			notes.save()
			return redirect('notes:detail',sub)
		else:
			form=NotesForm()
	else:
		form=NotesForm()
	context={
	'form':form,
	'subject':sub
	}
	return render(request,'notes/upload_notes.html',context)

def write_notes(request,*args,**kwargs):
	form=WriteNotesForm()
	sub=kwargs['subject']
	if request.method=='POST':
		form=WriteNotesForm(request.POST or None)
		if form.is_valid():
			
			notes=form.save(commit="False")
			notes.note_text = request.POST['note_text']
			notes.name=request.POST['name']
			notes.post_time = datetime.datetime.now()
			notes.student=get_object_or_404(Students,id=request.user.students.id)
			notes.subject=get_object_or_404(Subjects,id=sub)
			notes.save()
			return redirect('notes:detail',sub)
		else:
			form=WriteNotesForm()
	else:
		form=WriteNotesForm()
	context={
	'form':form,
	'subject':sub
	}
	return render(request,'notes/write_notes.html',context)

def view_written_notes(request,*args,**kwargs):
	id_=kwargs['pk']
	notes_=get_object_or_404(notes,id=id_)
	context={
		'notes':notes_
	}
	return render(request,'notes/notes_detail.html',context)


def edit_notes(request,*args,**kwargs):
	id_=kwargs['pk']
	context={}
	notes_=get_object_or_404(notes,id=id_)
	form=EditForm(request.POST or None, instance=notes_)
	if form.is_valid():
		form.save()
		return redirect('notes:view_notes',id_)
	context["form"]=form
	return render(request,'notes/edit_notes.html',context)



def delete_upload(request,*args,**kwargs):
	id_=kwargs['pk']

	notes_=get_object_or_404(notes,id=id_)
	sub=notes_.subject.id
	subject=get_object_or_404(Subjects,id=sub)
	
	notes_.delete()
	return redirect('notes:detail',sub)
	