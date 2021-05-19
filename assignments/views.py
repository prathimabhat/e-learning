from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import  Submission, Assignment,Message,Notification,Resources
from student_management.models import Subjects
from accounts.models import Students,Staffs
from django.shortcuts import render, HttpResponse, redirect
from .forms import AssignmentForm, NotificationForm, ResourceForm,MessageForm
import datetime
# Create your views here.

@login_required
def assignment(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    context={
        'subjects':subjects
    }
    return render(request,'staff_template/assignment.html',context)

@login_required
def resource(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    context={
        'subjects':subjects
    }
    return render(request,'staff_template/resource.html',context)

@login_required
def get_subject(request):
    sub=request.POST.get("subject")
    action=request.POST.get("action")
    subject=Subjects.objects.get(id=sub)
    sub_=subject.id
    if action=="view_assignment":
      
        return redirect('assignments:view_all_assignments',sub_)
    else:
        
        return redirect('assignments:add_assignment',sub_)
@login_required
def get_subject_student(request):
    sub=request.POST.get("subject")
    action=request.POST.get("action")
    subject=Subjects.objects.get(id=sub)
    sub_=subject.id
    if action=="view_assignment":
      
        return redirect('assignments:view_all_assignments',sub_)
    else:
        
        return redirect('assignments:add_assignment',sub_)

@login_required
def get_subject_resource(request):
    sub=request.POST.get("subject")
    subject=Subjects.objects.get(id=sub)
    sub_=subject.id
    return redirect('assignments:add_resource',sub_)

@login_required
def add_assignment(request, course_id):
    form = AssignmentForm(request.POST or None, request.FILES or None)
    course = Subjects.objects.get(id=course_id)
    if form.is_valid():
        assignment = form.save(commit=False)
        assignment.file = request.FILES['file']
        assignment.post_time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y')
        assignment.subject = course
        assignment.save()
        notification = Notification()
        notification.content = "New Assignment Uploaded"
        notification.subject = course
        notification.time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y')
        notification.save()
        return redirect('assignments:instructor_detail', course.id)

    return render(request, 'instructor/create_assignment.html', {'form': form, 'course': course})


## @brief view for the course's add-resource page.
#
# This view is called by <course_id>/add_resource url.\n
# It returns the webpage containing a form to add a resource and redirects to the course's detail page again after the form is submitted.
@login_required
def add_resource(request, course_id):
    form = ResourceForm(request.POST or None, request.FILES or None)
    instructor = Staffs.objects.get(user=request.user.id)
    course = Subjects.objects.get(id=course_id)
    if form.is_valid():
        resource = form.save(commit=False)
        resource.file_resource = request.FILES['file_resource']
        resource.subject = course
        resource.save()
        notification = Notification()
        notification.content = "New Resource Added - " + resource.title
        notification.subject = course
        notification.time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y')
        notification.save()
        course_=course.id
        return redirect('assignments:view_resources_staff', course_)

    return render(request, 'instructor/add_resource.html', {'form': form, 'course': course})

@login_required
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
@login_required
def view_all_assignments(request, course_id):
    course = Subjects.objects.get(id=course_id)
    assignments = Assignment.objects.filter(subject=course)
    return render(request, 'instructor/view_all_assignments.html', {'assignments' : assignments,'course': course})


## @brief view for the submissions page of an assignment.
#
# This view is called by <assignment_id>/view_all_submissions url.\n
# It returns the webpage containing links to all the submissions of an assignment.
@login_required
def view_all_submissions(request,assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)
    course = assignment.subject
    return render(request, 'instructor/view_all_submissions.html', {'submissions' : submissions,'course': course})


## @brief view for the feedback page containing an histogram of all the feddbacks provided by the students.
#
# This view is called by <assignment_id>/view_feedback url.\n
# It returns a webpage containing the feedback received by the students organized in the form of histogram.
@login_required
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


@login_required
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

@login_required
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
@login_required
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


@login_required
def view_assignments(request, course_id):
    course = Course.objects.get(id=course_id)
    assignments = Assignment.objects.filter(course=course)
    context = {
        'course' : course,
        'assignments' : assignments,
    }
    return render(request,'course/view_assignments.html',context)


## @brief view for the resources page of a course.
#
# This view is called by <course_id>/view_resources url.\n
# It returns the webpage containing all the resources of the course and links to download them.
@login_required
def view_resources(request, course_id):
    course = Course.objects.get(id=course_id)
    resources = Resources.objects.filter(course=course)
    context = {
        'course' : course,
        'resources' : resources,
    }
    return render(request,'course/view_resources.html',context)


## @brief view for the assignment's submission page.
#
# This view is called by <assignment_id>/upload_submission url.\n
# It returns the webpage containing a form to upload submission and redirects to the assignments page again after the form is submitted.
@login_required
def upload_submission(request, assignment_id):
    form = SubmissionForm(request.POST or None, request.FILES or None)
    assignment = Assignment.objects.get(id=assignment_id)
    course_id = assignment.course.id
    course = Course.objects.get(id=course_id)
    if form.is_valid():
        submission = form.save(commit=False)
        submission.user = request.user
        submission.assignment = assignment
        submission.time_submitted = datetime.datetime.now().strftime('%H:%M, %d/%m/%y')
        submission.save()
        return view_assignments(request, course_id)

    return render(request, 'course/upload_submission.html', {'form': form,'course': course})
