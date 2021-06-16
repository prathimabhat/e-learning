from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import  Submission, Assignment,Message,Notification,\
Resources,LectureLinks,Quiz,QuizQuestions,QuizChoice,QuizAnswers
from student_management.models import Subjects
from accounts.models import Students,Staffs
from django.shortcuts import render, HttpResponse, redirect
from accounts.decorators import staff_login_required,admin_login_required,student_login_required
from .forms import AssignmentForm, NotificationForm, ResourceForm,\
MessageForm,SubmissionForm,LecturelinksForm,QuizForm,QuizQuestionsForm,MCQForm
import datetime
from datetime import date, time
from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.contrib import messages

# Create your views here.


@staff_login_required
def assignment(request):
    subjects=Subjects.objects.filter(staff_id=request.user.staffs)
    context={
        'subjects':subjects
    }
    return render(request,'staff_template/assignment.html',context)

@staff_login_required
def resource(request):
    subjects=Subjects.objects.filter(staff_id=request.user.staffs)
    context={
        'subjects':subjects
    }
    return render(request,'staff_template/resource.html',context)

@student_login_required
def student_assignment(request):
    # subjects=Subjects.objects.filter(staff_id=request.user.id)
    
    student = Students.objects.get(user=request.user.id)
    course = student.course_id
    subjects = Subjects.objects.filter(course_id=course)
    context={
        'subjects':subjects
    }
    return render(request,'student_template/student_assignment.html',context)

@student_login_required
def student_resources(request):
    # subjects=Subjects.objects.filter(staff_id=request.user.id)
    
    student = Students.objects.get(user=request.user.id)
    course = student.course_id
    subjects = Subjects.objects.filter(course_id=course)
    context={
        'subjects':subjects
    }
    return render(request,'student_template/student_resources.html',context)
@staff_login_required
def get_subject(request):
    sub=request.POST.get("subject")
    action=request.POST.get("action")
    subject=Subjects.objects.get(id=sub)
    sub_=subject.id
    if action=="view_assignment":
      
        return redirect('assignments:view_all_assignments',sub_)
    else:
        
        return redirect('assignments:add_assignment',sub_)

@student_login_required
def get_subject_student(request):
    sub=request.POST.get("subject")
    action=request.POST.get("action")
    subject=Subjects.objects.get(id=sub)
    sub_=subject.id
    return redirect('assignments:view_assignments',sub_)
    # else:
        
    #     return redirect('assignments:upload_submission',sub_)

@student_login_required
def get_subject_student_resources(request):
    sub=request.POST.get("subject")
    action=request.POST.get("action")
    subject=Subjects.objects.get(id=sub)
    sub_=subject.id
    return redirect('assignments:view_resources',sub_)
    
@staff_login_required
def get_subject_resource(request):
    sub=request.POST.get("subject")
    action=request.POST.get("action")
    subject=Subjects.objects.get(id=sub)
    sub_=subject.id
    if action=="view_resource":
        return redirect('assignments:view_resources_staff', sub_)
    else:
        return redirect('assignments:add_resource',sub_)

from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail

@staff_login_required
def add_assignment(request, course_id):
    form = AssignmentForm(request.POST or None, request.FILES or None)
    domain=request.get_host()

    print(domain)
    print(request)
    course = Subjects.objects.get(id=course_id)
    stud=[]
    for i in course.student_id.all():
        stud.append(i)
    print(stud)
    if form.is_valid():
        assignment = form.save(commit=False)
        if(request.FILES):
            assignment.file = request.FILES['file']
        assignment.post_time = datetime.datetime.now()
        assignment.subject = course
        assignment.save()
        from_email = settings.EMAIL_HOST_USER
        ctx={
            "subjects":course,
            "domain":domain
        }
        html_message = render_to_string('course/send_email_assignment.html',ctx,request=request)
        plain_message = strip_tags(html_message)
        to_email=[]
        subject="New Assignment"
        for j in stud:
            print(j.user.email)
            to_email.append(j.user.email)
            print(to_email)
        mail.send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
        notification = Notification()
        notification.content = "New Assignment Uploaded"
        notification.subject = course
        notification.time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y')
        notification.save()
        return redirect('assignments:view_all_assignments', course.id)

    return render(request, 'instructor/create_assignment.html', {'form': form, 'course': course})


## @brief view for the course's add-resource page.
#
# This view is called by <course_id>/add_resource url.\n
# It returns the webpage containing a form to add a resource and redirects to the course's detail page again after the form is submitted.
@staff_login_required
def add_resource(request, course_id):
    form = ResourceForm(request.POST or None, request.FILES or None)
    instructor = Staffs.objects.get(user=request.user.id)
    course = Subjects.objects.get(id=course_id)
    domain=request.get_host()

    print(domain)
    stud=[]
    for i in course.student_id.all():
        stud.append(i)
    print(stud)
    if form.is_valid():
        resource = form.save(commit=False)
        if(request.FILES):
            resource.file_resource = request.FILES['file_resource']
        resource.subject = course
        resource.save()
        from_email = settings.EMAIL_HOST_USER
        ctx={
            "subjects":course,
            "domain":domain
        }
        html_message = render_to_string('course/send_email_resources.html',ctx,request=request)
        plain_message = strip_tags(html_message)
        to_email=[]
        subject="New Resource"
        for j in stud:
            print(j.user.email)
            to_email.append(j.user.email)
            print(to_email)
        mail.send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
        notification = Notification()
        notification.content = "New Resource Added - " + resource.title
        notification.subject = course
        notification.time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y')
        notification.save()
        course_=course.id
        
        return redirect('assignments:view_resources_staff', course_)

    return render(request, 'instructor/add_resource.html', {'form': form, 'course': course})



@staff_login_required
def gradeview(request,pk):
    domain=request.get_host()
    if request.method == 'POST':
        submission = Submission.objects.get(id=pk)
        submission.marks=request.POST.get('marks')
        
        assignment_id= submission.assignment.id
        submission.save()
        assignment=Assignment.objects.get(id=assignment_id)
        student=Students.objects.get(id=submission.user.id)
        from_email = settings.EMAIL_HOST_USER
        ctx={
            
            "domain":domain,
            "assignment":assignment,
            "submission":submission
        }
        html_message = render_to_string('course/send_email_assignment_grade.html',ctx,request=request)
        plain_message = strip_tags(html_message)
        to_email=[]
        subject="Assignment graded"
        to_email.append(student.user.email)
        mail.send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

        return redirect('assignments:view_all_submissions',assignment_id)
    else:
        print("hey")
        return render(request,'instructor/view_all_submissions.html')


@staff_login_required
def view_resources_staff(request, pk):
    course = Subjects.objects.get(id=pk)
    resources = Resources.objects.filter(subject=course)
    context = {
        'course' : course,
        'resources' : resources,
    }
    return render(request,'instructor/view_resources_staff.html',context)

## @brief view for the assignments page of a course.
#
# This view is called by <course_id>/view_all_assignments url.\n
# It returns the webpage containing all the assignments of the course and links to their submissions and feedbacks given by the students.
@staff_login_required
def view_all_assignments(request, course_id):
    course = Subjects.objects.get(id=course_id)
    assignments = Assignment.objects.filter(subject=course)
    return render(request, 'instructor/view_all_assignments.html', {'assignments' : assignments,'course': course})


## @brief view for the submissions page of an assignment.
#
# This view is called by <assignment_id>/view_all_submissions url.\n
# It returns the webpage containing links to all the submissions of an assignment.
@staff_login_required
def view_all_submissions(request,assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)
    course = assignment.subject
    return render(request, 'instructor/view_all_submissions.html', {'submissions' : submissions,'course': course})


## @brief view for the feedback page containing an histogram of all the feddbacks provided by the students.
#
# This view is called by <assignment_id>/view_feedback url.\n
# It returns a webpage containing the feedback received by the students organized in the form of histogram.
@staff_login_required
def view_feedback(request,assignment_id):
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    import matplotlib.ticker as ticker

    assignment = Assignment.objects.get(id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)

    feedbacks1 = list(map(lambda x: x.feedback, submissions)) #extract the feedbacks from the submissions list
    feedbacks = np.array(feedbacks1)

    fig = plt.figure(figsize=(10,6))
    fig.suptitle('Feedback received from the students', fontsize=16, fontweight='bold')
    fig.subplots_adjust(bottom=0.3)
    ax = fig.add_subplot(111)

    ax.set_xlabel('Rating(out of 10)')
    ax.set_ylabel('Number of Students')
    x = feedbacks
    ax.hist(x, bins=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], fc='lightblue', alpha=1, align='left', edgecolor='black', linewidth=1.0)
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1)) #sets the difference between adjacent y-tics

    plt.figtext(0.2, 0.1, 'Average Rating : '+ str(round(np.mean(feedbacks),2)),
                bbox={'facecolor': 'lightblue', 'alpha': 0.5, 'pad': 10})     #adds box in graph to display mean rating
    plt.figtext(0.5, 0.1, 'Number of Students Students who rated : ' + str(len(feedbacks1)),
                bbox={'facecolor': 'lightblue', 'alpha': 0.5, 'pad': 10})     #adds box in graph to display number of students who rated

    canvas = FigureCanvasAgg(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)  # converts the figure to http response
    return response


@staff_login_required
def add_notification(request, course_id):
    form = NotificationForm(request.POST or None)
    course = Subjects.objects.get(id=course_id)
    if form.is_valid():
        notification = form.save(commit=False)
        notification.subject = course
        notification.time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y') # get the current date,time and convert into string
        notification.save()
        return redirect('assignments:instructor_detail', course.id)

    return render(request, 'instructor/add_notification.html', {'course': course, 'form': form})

@staff_login_required
def instructor_index(request):
    user = request.user
    instructor = Staffs.objects.get(user=request.user.id)
    courses = Subjects.objects.filter(staff_id=instructor)
    context = {
        'user': user,
        'instructor': instructor,
        'courses': courses,
    }
    return render(request, 'instructor/instructor_index.html', context)


## @brief view for the detail page of the course.
#
# This view is called by <course_id>/instructor_detail url.\n
# It returns the course's detail page containing forum and links to add assignment,resource,notifications
# and view all the assignments and their submissions.
@staff_login_required
def instructor_detail(request, course_id):
    user = request.user
    instructor = Staffs.objects.get(user=request.user)
    courses = Subjects.objects.filter(staff_id=instructor.id)
    course = Subjects.objects.get(id=course_id)
    messages = Message.objects.filter(subject=course)
    form = MessageForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.subject = course
            message.sender = user
            message.time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y')
            message.save()
            try:
                student = Student.objects.get(user=request.user)
                return redirect('course:detail', course_id)

            except:
                return redirect('assignments:instructor_detail', course.id)

    else:
        form = MessageForm()

        context = {
                'user': user,
                'instructor': instructor,
                'course': course,
                'courses': courses,
                'messages': messages,
                'form' : form
            }

        return render(request, 'instructor/instructor_detail.html', context)

from django.utils import timezone
@student_login_required

def view_assignments(request, pk):
    course = Subjects.objects.get(id=pk)
    today_=timezone.localtime(timezone.now())
    print(today_)
    assignments = Assignment.objects.filter(subject=course)
    context = {
        'course' : course,
        'assignments' : assignments,
        'today':today_
    }
    return render(request,'course/view_assignments.html',context)


## @brief view for the resources page of a course.
#
# This view is called by <course_id>/view_resources url.\n
# It returns the webpage containing all the resources of the course and links to download them.
@student_login_required
def view_resources(request, course_id):
    course = Subjects.objects.get(id=course_id)
    resources = Resources.objects.filter(subject=course)
    context = {
        'course' : course,
        'resources' : resources,
    }
    return render(request,'course/view_resources.html',context)


## @brief view for the assignment's submission page.
#
# This view is called by <assignment_id>/upload_submission url.\n
# It returns the webpage containing a form to upload submission and redirects to the assignments page again after the form is submitted.
@student_login_required
def upload_submission(request, assignment_id):
    form = SubmissionForm(request.POST or None, request.FILES or None)
    assignment = Assignment.objects.get(id=assignment_id)
    course_id = assignment.subject.id
    domain=request.get_host()
    course = Subjects.objects.get(id=course_id)
    if form.is_valid():
        submission = form.save(commit=False)
        submission.user = request.user.students
        student=request.user.students
        student_=Students.objects.get(id=student.id)
        submission.assignment = assignment
        submission.time_submitted = datetime.datetime.now().strftime('%H:%M, %d/%m/%y')
        submission.save()
        from_email = settings.EMAIL_HOST_USER
        ctx={
            "subjects":course,
            "assignment":assignment,
            "students":student_,
            "domain":domain
        }
        html_message = render_to_string('instructor/send_email_submission.html',ctx,request=request)
        plain_message = strip_tags(html_message)
        subject="New Submission"
        to_email=[]
        to_email.append(course.staff_id.user.email)
        print(to_email)
        mail.send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

        return view_assignments(request, course_id)

    return render(request, 'course/upload_submission.html', {'form': form,'course': course})

@student_login_required
def detail(request, course_id):
    user = request.user
    student = Student.objects.get(user=request.user)
    courses = student.course_list.all()
    course = Course.objects.get(id=course_id)
    instructor = course.instructor
    messages = Message.objects.filter(course=course)
    form = MessageForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.course = course
            message.sender = user
            message.time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y') # get the current date,time and convert into string
            message.save()
            try:
                student = Student.objects.get(user=request.user)
                return redirect('course:detail', course_id)

            except:
                return redirect('instructor:instructor_detail', course.id)

    else:
        form = MessageForm()

        context = {
            'course': course,
            'user': user,
            'instructor': instructor,
            'student': student,
            'courses': courses,
            'messages': messages,
            'form': form
        }

        return render(request, 'course/detail.html', context)


@staff_login_required
def post_class_links(request,*args,**kwargs):
    form=LecturelinksForm(user=request.user.staffs)
    domain=request.get_host()
    if request.method=="POST":
        form=LecturelinksForm(request.POST ,user=request.user.staffs)
        if form.is_valid():
            sub=request.POST.get('subject')
            subject_= Subjects.objects.get(id=sub)
            form.save()
            stud=[]
            for i in subject_.student_id.all():
                stud.append(i)
            print(stud)
            from_email = settings.EMAIL_HOST_USER
            ctx={
                "subjects":subject_,
                "domain":domain
            }
            html_message = render_to_string('course/send_email_link.html',ctx,request=request)
            plain_message = strip_tags(html_message)
            to_email=[]
            subject="New Lecture URL"
            for j in stud:
                print(j.user.email)
                to_email.append(j.user.email)
                print(to_email)
            mail.send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
            return redirect('assignments:class_links')
        else:
            form=LecturelinksForm(user=request.user.staffs)
    else:
        form=LecturelinksForm(user=request.user.staffs)

    return render(request,'course/post_links.html',{'form':form})

@staff_login_required
def get_class_links_staff(request):
    sub_=Subjects.objects.filter(staff_id=request.user.staffs)
    link_=LectureLinks.objects.filter(subject__in=sub_)
    context={
        'subject':sub_,
        'links':link_
    }
    return render(request,'course/get_links_staff.html',context)

@student_login_required
def get_class_links_student(request):
    

    sub=Subjects.objects.filter(course_id=request.user.students.course_id)
    print(sub)
    links=LectureLinks.objects.filter(subject__in=sub)

    context={
        'subject':sub,
        'links':links
    }
    return render(request,'course/get_links_students.html',context)


@staff_login_required
def all_quizzes(request):
    quizzes=Quiz.objects.filter(staff=request.user.staffs)
    context={
    'quizzes':quizzes
    }
    return render(request,'instructor/all_quizzes.html',context)


@staff_login_required
def create_quiz(request):
    form=QuizForm(user=request.user.staffs)
    staff_=Staffs.objects.get(id=request.user.staffs.id)
    if request.method=="POST":
        form=QuizForm(request.POST,user=request.user.staffs)
        if form.is_valid():
            quiz = form.save(commit=False)
            sub=request.POST.get('subject')
            subject_= Subjects.objects.get(id=sub)
            quiz.subject=subject_
            quiz.staff=staff_
            quiz.save()
            
            return redirect('assignments:all_quizzes')
        else:
            form=QuizForm(user=request.user.staffs)
    else:
        form=QuizForm(user=request.user.staffs)

    return render(request,'instructor/create_quiz.html',{'form':form})

@staff_login_required
def select_question_type(request,pk):
    context={
        'quiz':pk
    }
    if request.method=="POST":
        type_=request.POST.get('qtn_type')
        if type_ =="subjective":
            return redirect('assignments:add_quiz_questions',pk)
        else:
            return redirect('assignments:add_mcq_questions',pk)
    return render(request,"instructor/select_question_type.html",context)


@staff_login_required
def get_quiz(request,pk):
    quiz_=Quiz.objects.get(id=pk)
    questions_=QuizQuestions.objects.filter(quiz=quiz_)
    choices=QuizChoice.objects.filter(question__in=questions_)
    context={
        'quiz':quiz_,
        'questions':questions_,
        'choices':choices
    }
    return render(request,'instructor/get_quiz.html',context)
'''
@staff_login_required
def edit_quiz(request,pk):
    form=EditQuizForm(obj=)
'''
@staff_login_required
def add_quiz_questions(request,pk):
    form=QuizQuestionsForm()
    quiz_=Quiz.objects.get(id=pk)
    if request.method=="POST":
        form=QuizQuestionsForm(request.POST)
        if form.is_valid():
            quizquestions = form.save(commit=False)
            quizquestions.quiz=quiz_
            quizquestions.question_type="subjective"
            quizquestions.save()
           
            return redirect('assignments:get_quiz',pk)
        else:
            form=QuizQuestionsForm()
    else:
        form=QuizQuestionsForm()

    return render(request,'instructor/create_quiz_questions.html',{'form':form})

@staff_login_required
def add_mcq_questions(request,pk):
    form=QuizQuestionsForm()
    quiz_=Quiz.objects.get(id=pk)
    if request.method=="POST":
        form=QuizQuestionsForm(request.POST)
        if form.is_valid():
            quizquestions = form.save(commit=False)
            quizquestions.quiz=quiz_
            quizquestions.question_type="objective"
            quizquestions.save()
            
            return redirect('assignments:get_quiz',pk)
        else:
            form=QuizQuestionsForm()
    else:
        form=QuizQuestionsForm()

    return render(request,'instructor/create_quiz_questions.html',{'form':form})

@staff_login_required
def add_choices(request,pk):
    qtn=QuizQuestions.objects.get(id=pk)
    form=MCQForm()
    if request.method =="POST":
        form=MCQForm(request.POST)
        if form.is_valid():
            choice=form.save(commit=False)
            choice.question=qtn
            choice.save()
            id_=qtn.quiz.id
            return redirect('assignments:get_quiz',id_)
        else:
            form=MCQForm()
    else:
        form=MCQForm()

    return render(request,'instructor/create_mcqs.html',{'form':form})

@staff_login_required
def enable_quiz(request,pk):
    quiz_=Quiz.objects.get(id=pk)
    quiz_.enable=True
    quiz_.save()
    return redirect('assignments:all_quizzes')

@staff_login_required
def disable_quiz(request,pk):
    quiz_=Quiz.objects.get(id=pk)
    quiz_.enable=False
    quiz_.save()
    return redirect('assignments:all_quizzes')

@student_login_required
def all_quizzes_students(request):
    sub=Subjects.objects.filter(course_id=request.user.students.course_id)
    quizzes=Quiz.objects.filter(subject__in=sub)
    context={
        'quizzes':quizzes
    }
    return render(request,'course/all_quizzes_students.html',context)



@student_login_required
def get_quiz_students(request,pk):
    quiz_=Quiz.objects.get(id=pk)
    questions=QuizQuestions.objects.filter(quiz=quiz_)
    choices=QuizChoice.objects.filter(question__in=questions)
    

    context={
        'quiz':quiz_,
        'questions':questions,
        'choices':choices,
        }

    return render(request,'course/get_quiz_students.html',context)

@student_login_required
def quiz_question_detail(request,quiz_id,question_id):
    quiz=Quiz.objects.get(id=quiz_id)
    qtn=QuizQuestions.objects.get(id=question_id)
    all_questions=QuizQuestions.objects.filter(quiz=quiz)
    number_of_questions=all_questions.count()+1
    range_=range(1,number_of_questions)
    list_=zip(all_questions,range_)
    if(QuizAnswers.objects.filter(question=qtn,student=request.user.students).exists()):
   
        status=True
    else:
        status=False

    if(qtn.question_type == "objective"):
        choice=QuizChoice.objects.get(question=qtn)
        context={
            'quiz':quiz,
            'question':qtn,
            'choice':choice,
            'status':status,
            'list':list_
        }
    else:
        context={
            'quiz':quiz,
            'question':qtn,
            'status':status,
            'all_questions':all_questions,
            'range':range_
            }

    return render(request,'course/quiz_question_detail.html',context)


@student_login_required
def quiz_answer_save(request,quiz_id,question_id):
    if request.method=="POST":
        quiz_=Quiz.objects.get(id=quiz_id)
        qtn=QuizQuestions.objects.get(id=question_id)
        student_=Students.objects.get(id=request.user.students.id)
        answer_=request.POST.get('answer')
        try:
            ans=QuizAnswers(quiz=quiz_,student=student_,answer_text=answer_,question=qtn)
            ans.save()
          
            
            return redirect('assignments:quiz_question_detail',quiz_id,question_id)
        except:
            messages.error(request, "Failed to submit answer")
            
            return redirect('assignments:quiz_question_detail',quiz_id,question_id)
    
    return render(request,'course/get_quiz_students.html')

@staff_login_required
def view_quiz_submissions(request,quiz_id):
    quiz_=Quiz.objects.get(id=quiz_id)
    submissions=QuizAnswers.objects.filter(quiz=quiz_)
    students=set()
    for x in submissions:
        students.add(x.student)

    context={
        'quiz':quiz_,
        'students':students
        
    }
    return render(request,'instructor/view_quiz_submissions.html',context)

@staff_login_required
def get_submission_detail(request,quiz_id,student_id):
    quiz_=Quiz.objects.get(id=quiz_id)
    stu=Students.objects.get(id=student_id)
    submission=QuizAnswers.objects.filter(quiz=quiz_).filter(student=stu)
    context={
    'submission':submission
    }
    return render(request,'instructor/get_submission_detail.html',context)