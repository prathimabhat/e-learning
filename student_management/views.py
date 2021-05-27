from django.shortcuts import render
import datetime
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Students,CustomUser , SessionYearModel,Parents,Staffs,AdminHOD
from student_management.models import Courses, Subjects,  Attendance, AttendanceReport,FeedBackStudent, LeaveReportStudent, NotificationStudent, StudentResult


#AdminHod views 
    

def admin_home(request):
    student_count1 = Students.objects.all().count()
    staff_count = Staffs.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()

    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []
    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subjects_all:
        course = Courses.objects.get(id=subject.course_id.id)
        student_count = Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    staffs = Staffs.objects.all()
    attendance_present_list_staff = []
    attendance_absent_list_staff = []
    staff_name_list = []
    for staff in staffs:
        subject_ids = Subjects.objects.filter(staff_id=staff.user.id)
        attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.user.username)

    students_all = Students.objects.all()
    attendance_present_list_student = []
    attendance_absent_list_student = []
    student_name_list = []
    for student in students_all:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves + absent)
        student_name_list.append(student.user.username)

    return render(request, "hod_template/main_content.html",
                  {"student_count": student_count1, "staff_count": staff_count, "subject_count": subject_count,
                   "course_count": course_count, "course_name_list": course_name_list,
                   "subject_count_list": subject_count_list,
                   "student_count_list_in_course": student_count_list_in_course,
                   "student_count_list_in_subject": student_count_list_in_subject, "subject_list": subject_list,
                   "staff_name_list": staff_name_list, "attendance_present_list_staff": attendance_present_list_staff,
                   "attendance_absent_list_staff": attendance_absent_list_staff, "student_name_list": student_name_list,
                   "attendance_present_list_student": attendance_present_list_student,
                   "attendance_absent_list_student": attendance_absent_list_student})





def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        qualification = request.POST.get("qualification")
        dob = request.POST.get("dob")
        blood_group = request.POST.get("blood_group")
        teacher_roll_number = request.POST.get("teacher_roll_number")
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        ph_no = request.POST.get("ph_no")

        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)
        staff_name=first_name+last_name
        try:
            user = CustomUser.objects.create_user( email=email,password=password, user_type='2',
                first_name=first_name,last_name=last_name)
            user.save()
            user.refresh_from_db()
            user.staffs.staff_name=staff_name
            user.staffs.gender = gender
            user.staffs.address = address
            user.staffs.ph_no = ph_no
            user.staffs.dob = dob
            user.staffs.qualification = qualification
            user.staffs.blood_group = blood_group
            user.staffs.teacher_roll_number = teacher_roll_number
            user.staffs.profile_pic = profile_pic_url
            user.staffs.save()
            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))


def add_course(request):
    return render(request, "hod_template/add_course_template.html")


def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course = request.POST.get("course")
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request, "Failed to Add Course")
            return HttpResponseRedirect(reverse("add_course"))


def add_student(request):
    courses = Courses.objects.all()
    sessions = SessionYearModel.objects.all()
    return render(request, "hod_template/add_student_template.html", {"courses": courses, "sessions": sessions})


def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name = request.POST.get("first_name")
        password = request.POST.get("password")
        last_name = request.POST.get("last_name")
        #username = request.POST.get("username")
        #parent_username = request.POST.get("parent_username")
        blood_group = request.POST.get("blood_group")
        email = request.POST.get("email")
        address = request.POST.get("address")
        roll_number = request.POST.get("roll_number")
        # parent_roll_number = request.POST.get("parent_roll_number")
        gender = request.POST.get("gender")
        ph_no = request.POST.get("ph_no")
        dob = request.POST.get("dob")
        session_year_id = request.POST.get("session_year_id")
        course_id = request.POST.get("course")
        parent_email = request.POST.get("parent_email")
        parent_address = request.POST.get("parent_address")
        parent_password = request.POST.get("parent_password")
        father_name = request.POST.get("father_name")
        mother_name = request.POST.get("mother_name")
        father_occupation = request.POST.get("father_occupation")
        mother_occupation = request.POST.get("mother_occupation")
        parent_ph_no = request.POST.get("parent_ph_no")

        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)
        student_name=first_name+last_name
        try:
            user = CustomUser.objects.create_user( email=email,password=password, user_type='3',
                                                   last_name=last_name, first_name=first_name)
            user.save()

            user1 = CustomUser.objects.create_user( email=parent_email, password=parent_password,user_type='4')
            user1.save()

            user.refresh_from_db()
            user.students.student_name=student_name                                     
            user.students.address = address
            course_obj = Courses.objects.get(id=course_id)
            user.students.course_id = course_obj 
            user.students.gender = gender
            user.students.roll_number = roll_number
            user.students.dob = dob
            user.students.blood_group = blood_group
            user.students.ph_no = ph_no
            user.students.profile_pic = profile_pic_url
            session_year = SessionYearModel.objects.get(id=session_year_id)
            user.students.session_year_id = session_year

            user.students.save()
            stu_id=Students.objects.get(id=user.students.id)
            user1.refresh_from_db()
            user1.parents.father_name=father_name
            user1.parents.mother_name=mother_name
            user1.parents.parent_ph_no = parent_ph_no
            user1.parents.father_occupation = father_occupation
            user1.parents.mother_occupation = mother_occupation
            user1.parents.parent_address = parent_address
            user1.parents.parent_of=stu_id  
            user1.parents.save()

            messages.success(request, "Successfully Added Student Details")
            return HttpResponseRedirect(reverse("add_student"))
        except:
            messages.error(request, "Failed to Add Student Details")
            return HttpResponseRedirect(reverse("add_student"))


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/add_subject_template.html", {"staffs": staffs, "courses": courses})


def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)
        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))


def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, "hod_template/manage_staff_template.html", {"staffs": staffs})


def manage_student(request):
    course = request.POST.get("course")
    students = Students.objects.filter(course_id=course)
    parents = Parents.objects.all()
    return render(request, "hod_template/manage_student_template.html", {"students": students, "parents": parents})

def manage_course(request):
    courses = Courses.objects.all()
    return render(request, "hod_template/manage_course_template.html", {"courses": courses})


def manage_subject(request):
    course = request.POST.get("course")
    subjects = Subjects.objects.filter(course_id=course)
    return render(request, "hod_template/manage_subject_template.html", {"subjects": subjects})


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(user=staff_id)
    return render(request, "hod_template/edit_staff_template.html", {"staff": staff, "id": staff_id})


def edit_staff_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        dob = request.POST.get("dob")
        qualification = request.POST.get("qualification")
        blood_group = request.POST.get("blood_group")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        ph_no = request.POST.get("ph_no")
        teacher_roll_number = request.POST.get("teacher_roll_number")

        if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            staff_model = Staffs.objects.get(user=staff_id)
            staff_model.address = address
            staff_model.dob = dob
            staff_model.qualification = qualification
            staff_model.blood_group = blood_group
            staff_model.teacher_roll_number = teacher_roll_number
            if profile_pic_url != None:
                staff_model.profile_pic = profile_pic_url
            staff_model.gender = gender
            staff_model.ph_no = ph_no
            staff_model.save()
            messages.success(request, "Successfully Updated Staff Details")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))
        except:
            messages.error(request, "Failed to Edit Staff Details")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))


def edit_student(request, student_id):
    student = Students.objects.get(user=student_id)
    x = int(student_id) + 1
    courses = Courses.objects.all()
    sessions = SessionYearModel.objects.all()
    parents = Parents.objects.get(user=str(x))
    print(student_id, x)
    return render(request, "hod_template/edit_student_template.html",
                  {"student": student, "courses": courses, "sessions": sessions, "id": student_id, "parents": parents})


def edit_student_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        address = request.POST.get("address")
        roll_number = request.POST.get("roll_number")
        gender = request.POST.get("gender")
        ph_no = request.POST.get("ph_no")
        dob = request.POST.get("dob")
        session_year_id = request.POST.get("session_year_id")
        course_id = request.POST.get("course")
        parent_email = request.POST.get("parent_email")
        parent_address = request.POST.get("parent_address")
        father_name = request.POST.get("father_name")
        mother_name = request.POST.get("mother_name")
        father_occupation = request.POST.get("father_occupation")
        mother_occupation = request.POST.get("mother_occupation")
        parent_ph_no = request.POST.get("parent_ph_no")
        parent_username = request.POST.get("parent_username")

        if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            x = int(student_id) + 1
            user = CustomUser.objects.get(id=student_id)
            user1 = CustomUser.objects.get(id=str(x))

            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            user1.first_name = father_name
            user1.last_name = mother_name
            user1.username = parent_username
            user1.email = parent_email
            user1.save()

            student = Students.objects.get(user=student_id)
            parent = Parents.objects.get(user=str(x))

            parent.parent_address = parent_address
            parent.ph_no = parent_ph_no
            parent.father_occupation = father_occupation
            parent.mother_occupation = mother_occupation
            parent.save()

            student.address = address
            session_year = SessionYearModel.objects.get(id=session_year_id)
            student.session_year_id = session_year
            student.gender = gender
            student.roll_number = roll_number
            student.dob = dob
            student.ph_no = ph_no
            course = Courses.objects.get(id=course_id)
            student.course_id = course

            if profile_pic_url != None:
                student.profile_pic = profile_pic_url

            student.save()

            # del request.session['student_id']
            messages.success(request, "Successfully Updated Student Details")
            return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))
        except:
            messages.error(request, "Failed to Edit Student Details")
            return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/edit_subject_template.html",
                  {"subject": subject, "staffs": staffs, "courses": courses, "id": subject_id})


def edit_subject_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")
        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            subject.save()
            messages.success(request, "Successfully Updated Subject Details")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))
        except:
            messages.error(request, "Failed to Edit Subject Details")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(request, "hod_template/edit_course_template.html", {"course": course, "id": course_id})


def edit_course_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course")
        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, "Successfully Updated Course Details")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id": course_id}))
        except:
            messages.error(request, "Failed to Edit Course Details")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id": course_id}))


def manage_session(request):
    return render(request, "hod_template/manage_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_parent_email_exist(request):
    email = request.POST.get("parent_email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_roll_number_exist(request):
    roll_number = request.POST.get("roll_number")
    user_obj = Students.objects.filter(roll_number=roll_number).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


'''@csrf_exempt
def check_parent_roll_number_exist(request):
    parent_roll_number = request.POST.get("parent_roll_number")
    user_obj = Parents.objects.filter(parent_roll_number=parent_roll_number).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)'''


@csrf_exempt
def check_teacher_roll_number_exist(request):
    teacher_roll_number = request.POST.get("teacher_roll_number")
    user_obj = Staffs.objects.filter(teacher_roll_number=teacher_roll_number).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_parent_username_exist(request):
    username = request.POST.get("parent_username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    return render(request, "hod_template/staff_feedback_template.html", {"feedbacks": feedbacks})


def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    return render(request, "hod_template/student_feedback_template.html", {"feedbacks": feedbacks})


@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def parent_feedback_message(request):
    feedbacks = FeedBackParent.objects.all()
    return render(request, "hod_template/parent_feedback_template.html", {"feedbacks": feedbacks})


@csrf_exempt
def parent_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackParent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    return render(request, "hod_template/staff_leave_view.html", {"leaves": leaves})


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    return render(request, "hod_template/student_leave_view.html", {"leaves": leaves})


def student_approve_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def student_disapprove_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_approve_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def staff_disapprove_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def admin_view_attendance(request):
    course = request.POST.get("course")
    # print(course)
    subjects = Subjects.objects.filter(course_id=course)
    # subject2 = Subjects.objects.get(staff_id=request.user.id)
    #subjects = Subjects.objects.filter(course_id=course).filter(staff_id=request.user.id)
    #session_years = SessionYearModel.object.all()
    #return render(request, "staff_template/staff_take_attendance.html",
                  #{"subjects": subjects, "session_years": session_years})
    #subjects = Subjects.objects.all()
    session_year_id = SessionYearModel.objects.all()
    return render(request, "hod_template/admin_view_attendance.html",
                  {"subjects": subjects, "session_year_id": session_year_id})


@csrf_exempt
def admin_get_attendance_dates(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")
    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(subject_id=subject_obj, session_year_id=session_year_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date),
                "session_year_id": attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for student in attendance_data:
        data_small = {"id": student.student_id.user.id,
                      "name": student.student_id.user.first_name + " " + student.student_id.user.last_name,
                      "status": student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "hod_template/admin_profile.html", {"user": user})


def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))


def select_student_class(request):
    courses = Courses.objects.all()
    return render(request, "hod_template/select_student_class_template.html", {"courses": courses})

def select_attendance_class(request):
    courses = Courses.objects.all()
    return render(request, "hod_template/select_attendance_class_template.html", {"courses": courses})

def select_subject(request):
    courses = Courses.objects.all()
    return render(request, "hod_template/select_subject_template.html", {"courses": courses})


def admin_send_notification_student(request):
    student = Students.objects.all()
    return render(request, "hod_template/student_notification.html", {"students": student})

def admin_send_notification_parent(request):
    parent = Parents.objects.all()
    return render(request, "hod_template/parent_notification.html", {"parents": parent})

def admin_send_notification_staff(request):
    staff = Staffs.objects.all()
    return render(request, "hod_template/staff_notification.html", {"staffs": staff})


@csrf_exempt
def send_student_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    student = Students.objects.get(user=id)
    token = student.fcm_token
    url = "https://fcm.googleapis.com/fcm/send"
    body = {
        "notification": {
            "title": "Student Management System",
            "body": message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/student_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to": token
    }
    headers = {"Content-Type": "application/json",
               "Authorization": "key=AAAA8jHrBqI:APA91bFFHtJXpd6HkmhHFAhr2WTO0A3_c1JWPK1Bv5FeJo1mmZ32Ck9chrfixaFEiPB0RfP0xuUUwbeRUiiFBAI5i3GYo-VrlyIxaM-pAD7NteXDfzCYxd6g944M-66MnIWnMx0hHLwB"}
    data = request.post(url, data=json.dumps(body), headers=headers)
    notification = NotificationStudent(student_id=student, message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")

@csrf_exempt
def send_parent_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    parent = Parents.objects.get(user=id)
    token = parent.fcm_token
    url = "https://fcm.googleapis.com/fcm/send"
    body = {
        "notification": {
            "title": "Student Management System",
            "body": message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/parent_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to": token
    }
    headers = {"Content-Type": "application/json",
               "Authorization": "key=AAAA8jHrBqI:APA91bFFHtJXpd6HkmhHFAhr2WTO0A3_c1JWPK1Bv5FeJo1mmZ32Ck9chrfixaFEiPB0RfP0xuUUwbeRUiiFBAI5i3GYo-VrlyIxaM-pAD7NteXDfzCYxd6g944M-66MnIWnMx0hHLwB"}
    data = request.post(url, data=json.dumps(body), headers=headers)
    notification = NotificationParent(parent_id=parent, message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")

@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    staff = Staffs.objects.get(user=id)
    token = staff.fcm_token
    url = "https://fcm.googleapis.com/fcm/send"
    body = {
        "notification": {
            "title": "Student Management System",
            "body": message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/staff_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to": token
    }
    headers = {"Content-Type": "application/json",
               "Authorization": "key=AAAA8jHrBqI:APA91bFFHtJXpd6HkmhHFAhr2WTO0A3_c1JWPK1Bv5FeJo1mmZ32Ck9chrfixaFEiPB0RfP0xuUUwbeRUiiFBAI5i3GYo-VrlyIxaM-pAD7NteXDfzCYxd6g944M-66MnIWnMx0hHLwB"}
    data = request.post(url, data=json.dumps(body), headers=headers)
    notification = NotificationStaffs(staff_id=staff, message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")


def delete_student(request, student_id):
    # student = Students.objects.get(id=student_id)
    # student.delete()
    user = CustomUser.objects.get(id=student_id)
    x = int(student_id) + 1
    user1 = CustomUser.objects.get(id=str(x))
    print(student_id, x)
    user.delete()
    user1.delete()
    return HttpResponseRedirect("/select_student_class")


def delete_staff(request, staff_id):
    user = CustomUser.objects.get(id=staff_id)
    user.delete()
    return HttpResponseRedirect(reverse("manage_staff"))


def delete_course(request, course_id):
    user = Courses.objects.get(id=course_id)
    user.delete()
    # return HttpResponseRedirect("/manage_course")
    # return render(request, "hod_template/manage_course_template.html", {"id": course_id})
    return HttpResponseRedirect(reverse("manage_course"))


def delete_subject(request, subject_id):
    user = Subjects.objects.get(id=subject_id)
    user.delete()
    return HttpResponseRedirect("/select_subject")






#student views

def student_home(request):
    student_obj = Students.objects.get(user=request.user.id)
    attendance_total = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()
    course = Courses.objects.get(id=student_obj.course_id.id)
    subjects = Subjects.objects.filter(course_id=course).count()

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True,
                                                                   student_id=student_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False,
                                                                  student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    return render(request, "student_template/student_main_content.html",
                  {"total_attendance": attendance_total, "attendance_absent": attendance_absent,
                   "attendance_present": attendance_present, "subjects": subjects, "data_name": subject_name,
                   "data1": data_present, "data2": data_absent})


def student_view_attendance(request):
    student = Students.objects.get(user=request.user.id)
    course = student.course_id
    subjects = Subjects.objects.filter(course_id=course)
    return render(request, "student_template/student_view_attendance.html", {"subjects": subjects})


def student_view_attendance_post(request):
    subject_id = request.POST.get("subject")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    start_date_parse = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_parse = datetime.strptime(end_date, "%Y-%m-%d").date()


    subject_obj = Subjects.objects.get(id=subject_id)
    user_obj = CustomUser.objects.get(id=request.user.id)
    stud_obj = Students.objects.get(user=user_obj)

    attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse),
                                           subject_id=subject_obj)
    attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)

    return render(request, "student_template/student_attendance_data.html", {"attendance_reports": attendance_reports})


def student_apply_leave(request):
    staff_obj = Students.objects.get(user=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=staff_obj)
    return render(request, "student_template/student_apply_leave.html", {"leave_data": leave_data})


def student_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")

        student_obj = Students.objects.get(user=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_msg,
                                              leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))


def student_feedback(request):
    staff_id = Students.objects.get(user=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=staff_id)
    return render(request, "student_template/student_feedback.html", {"feedback_data": feedback_data})


def student_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg = request.POST.get("feedback_msg")

        student_obj = Students.objects.get(user=request.user.id)
        try:
            feedback = FeedBackStudent(student_id=student_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(user=user)
    user1 = int(request.user.id) + 1
    user2 = CustomUser.objects.get(id=str(user1))
    parent = Parents.objects.get(user=user2)
    print(user, user1)
    return render(request, "student_template/student_profile.html",
                  {"user": user, "user2": user2, "student": student, "parent": parent})


def student_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        '''
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        address = request.POST.get("address")
        dob = request.POST.get("dob")
        ph_no = request.POST.get("ph_no")
        gender = request.POST.get("gender")
        '''
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            # customuser.first_name = first_name
            # customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            '''
            student = Students.objects.get(admin=customuser)
            student.address = address
            student.dob = dob
            student.gender = gender
            student.ph_no = ph_no
            student.save()
            '''
            #messages.success(request, "Successfully Updated Password")
            return HttpResponseRedirect(reverse("login"))
        except:
            #messages.error(request, "Failed to Update Password")
            return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def student_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        student = Students.objects.get(user=request.user.id)
        student.fcm_token = token
        student.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def student_all_notification(request):
    student = Students.objects.get(user=request.user.id)
    notifications = NotificationStudent.objects.filter(student_id=student.id)
    return render(request, "student_template/all_notification.html", {"notifications": notifications})


def student_view_result(request):
    student = Students.objects.get(user=request.user.id)
    studentresult = StudentResult.objects.filter(student_id=student.id)
    return render(request, "student_template/student_result.html", {"studentresult": studentresult})



# staff views
import json
from datetime import datetime
from uuid import uuid4

from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from student_management.models import Subjects, SessionYearModel, LeaveReportStaff,  FeedBackStaffs, NotificationStaffs




def staff_home(request):
    # For Fetch All Student Under Staff
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)

    final_course = []
    # removing Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count = Students.objects.filter(course_id__in=final_course).count()

    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()

    # Fetch All Approve Leave
    staff = Staffs.objects.get(user=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
    subject_count = subjects.count()

    # Fetch Attendance Data by Subject
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance = Students.objects.filter(course_id__in=final_course)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
        student_list.append(student.user.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    return render(request, "staff_template/staff_main_content.html",
                  {"students_count": students_count, "attendance_count": attendance_count, "leave_count": leave_count,
                   "subject_count": subject_count, "subject_list": subject_list, "attendance_list": attendance_list,
                   "student_list": student_list, "present_list": student_list_attendance_present,
                   "absent_list": student_list_attendance_absent})


def staff_take_attendance(request):
    # print(request.user.id)
    course = request.POST.get("course")
    # print(course)
    # subject1 = Subjects.objects.get(course_id=course)
    # subject2 = Subjects.objects.get(staff_id=request.user.id)
    subjects = Subjects.objects.filter(course_id=course).filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    return render(request, "staff_template/staff_take_attendance.html",
                  {"subjects": subjects, "session_years": session_years})


def select_class(request):
    courses = Courses.objects.all()
    return render(request, "staff_template/select_class_template.html",
                  {"courses": courses})



def edit_select_class(request):
    courses = Courses.objects.all()
    return render(request, "staff_template/edit_select_class_template.html", {"courses": courses})


@csrf_exempt
def get_students(request):
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year")

    subject = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.objects.get(id=session_year)
    students = Students.objects.filter(course_id=subject.course_id, session_year_id=session_model)
    list_data = []

    for student in students:
        data_small = {"id": student.user.id, "roll_number": student.roll_number,
                      "name": student.user.first_name + " " + student.user.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_attendance_data(request):
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")

    subject_model = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.objects.get(id=session_year_id)
    json_sstudent = json.loads(student_ids)
    # print(data[0]['id'])

    try:
        attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date,
                                session_year_id=session_model)
        attendance.save()

        for stud in json_sstudent:
            student = Students.objects.get(user=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def staff_update_attendance(request):
    course = request.POST.get("course")
    subjects = Subjects.objects.filter(course_id=course).filter(staff_id=request.user.id)
    session_year_id = SessionYearModel.objects.all()
    return render(request, "staff_template/staff_update_attendance.html",
                  {"subjects": subjects, "session_year_id": session_year_id})


@csrf_exempt
def get_attendance_dates(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")
    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(subject_id=subject_obj, session_year_id=session_year_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date),
                "session_year_id": attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for student in attendance_data:
        data_small = {"id": student.student_id.user.id,
                      "name": student.student_id.user.first_name + " " + student.student_id.user.last_name,
                      "status": student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_updateattendance_data(request):
    student_ids = request.POST.get("student_ids")
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_sstudent = json.loads(student_ids)
    try:
        for stud in json_sstudent:
            student = Students.objects.get(user=stud['id'])
            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status = stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(user=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    return render(request, "staff_template/staff_apply_leave.html", {'leave_data': leave_data})


def staff_apply_leave_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_message = request.POST.get("leave_message")

        staff_obj = Staffs.objects.get(user=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message,
                                            leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
            messages.error(request, "Failed to Apply for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))


def staff_feedback(request):
    staff_id = Staffs.objects.get(user=request.user.id)
    feedback_data = FeedBackStaffs.objects.filter(staff_id=staff_id)
    return render(request, "staff_template/staff_feedback.html", {"feedback_data": feedback_data})


def staff_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_feedback"))
    else:
        feedback_message = request.POST.get("feedback_message")

        staff_obj = Staffs.objects.get(user=request.user.id)
        try:
            feedback = FeedBackStaffs(staff_id=staff_obj, feedback=feedback_message, feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))


def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(user=user)
    return render(request, "staff_template/staff_profile.html", {"user": user, "staff": staff})


def staff_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        '''
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")   
        ph_no = request.POST.get("ph_no")
        gender = request.POST.get("gender")
        '''
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            '''
            customuser.first_name = first_name
            customuser.last_name = last_name
            '''
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            '''
            staff = Staffs.objects.get(user=customuser.id)
            staff.address = address
            staff.gender = gender
            staff.ph_no = ph_no
            staff.save()
            '''
            #messages.success(request, "Successfully Updated Password")
            return HttpResponseRedirect(reverse("login"))
        except:
            messages.error(request, "Failed to Update Password")
            #return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def staff_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        staff = Staffs.objects.get(user=request.user.id)
        staff.fcm_token = token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def staff_all_notification(request):
    staff = Staffs.objects.get(user=request.user.id)
    notifications = NotificationStaffs.objects.filter(staff_id=staff.id)
    return render(request, "staff_template/all_notification.html", {"notifications": notifications})


def staff_add_result(request):
    # course = request.POST.get("course")
    # subjects = Subjects.objects.filter(course_id=course).filter(staff_id=request.user.id)
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    courses = Courses.objects.all()
    session_years = SessionYearModel.objects.all()
    return render(request, "staff_template/staff_add_result.html",
                  {"subjects": subjects, "courses": courses, "session_years": session_years})


def save_student_result(request):
    subject = request.POST.get("subject")
    print(subject)
    if request.method != 'POST':
        return HttpResponseRedirect('staff_add_result')
    student_user_id = request.POST.get('student_list')
    assignment_marks = request.POST.get('assignment_marks')
    exam_marks = request.POST.get('exam_marks')
    subject_id = request.POST.get('subject')

    student_obj = Students.objects.get(user=student_user_id)
    subject_obj = Subjects.objects.get(id=subject_id)

    try:
        check_exist = StudentResult.objects.filter(subject_id=subject_obj, student_id=student_obj).exists()
        if check_exist:
            result = StudentResult.objects.get(subject_id=subject_obj, student_id=student_obj)
            result.subject_assignment_marks = assignment_marks
            result.subject_exam_marks = exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("staff_add_result"))
        else:
            result = StudentResult(student_id=student_obj, subject_id=subject_obj, subject_exam_marks=exam_marks,
                                   subject_assignment_marks=assignment_marks)
            result.save()
            messages.success(request, "Successfully Added Result")
            return HttpResponseRedirect(reverse("staff_add_result"))
    except:
        messages.error(request, "Failed to Add Result")
        return HttpResponseRedirect(reverse("staff_add_result"))


@csrf_exempt
def fetch_result_student(request):
    subject_id = request.POST.get('subject_id')
    student_id = request.POST.get('student_id')
    student_obj = Students.objects.get(user=student_id)
    result = StudentResult.objects.filter(student_id=student_obj.id, subject_id=subject_id).exists()
    if result:
        result = StudentResult.objects.get(student_id=student_obj.id, subject_id=subject_id)
        result_data = {"exam_marks": result.subject_exam_marks, "assign_marks": result.subject_assignment_marks}
        return HttpResponse(json.dumps(result_data))
    else:
        return HttpResponse("False")

def edit_result_select_class_session(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    courses = Courses.objects.all()
    session_years = SessionYearModel.objects.all()
    return render(request, "staff_template/edit_result_select_class_session.html",
                  {"subjects": subjects, "courses": courses, "session_years": session_years})


def manage_student_result_list_display(request):
    course = request.POST.get("course")
    print(course)
    session_year = request.POST.get("session_year")
    results = StudentResult.objects.all()
    students = Students.objects.filter(course_id=course).filter(session_year_id=session_year)
    return render(request, "staff_template/manage_student_result_list_display.html", {"students": students, "results": results})


def edit_student_result(request, student_id):
    student = Students.objects.get(id=student_id)
    # courses = Courses.objects.all()
    # sessions = SessionYearModel.object.all()
    results = StudentResult.objects.get(student_id= student_id)
    return render(request, "staff_template/edit_student_result.html",
                  {"student": student, "id": student_id,  "results": results})


def edit_student_result_save(request):
    student_id = request.POST.get("student_id")
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_assignment_marks = request.POST.get('subject_assignment_marks')
        subject_exam_marks = request.POST.get('subject_exam_marks')
        try:
            results = StudentResult.objects.get(student_id=student_id)
            results.subject_assignment_marks = subject_assignment_marks
            results.subject_exam_marks = subject_exam_marks
            results.save()
            messages.success(request, "Successfully Updated Results")
            return HttpResponseRedirect(reverse("edit_student_result", kwargs={"student_id": student_id}))
        except:
            messages.error(request, "Failed to Update Results")
            return HttpResponseRedirect(reverse("edit_student_result", kwargs={"student_id": student_id}))



#parent views

from student_management.models import FeedBackParent, NotificationParent



def parent_home(request):
    return render(request, "parent_template/parent_main_content.html")

def parent_view_attendance(request):
    x = int(request.user.id) - 1
    student = Students.objects.get(user=str(x))
    course = student.course_id
    subjects = Subjects.objects.filter(course_id=course)
    return render(request, "parent_template/parent_view_attendance.html", {"subjects": subjects})


def parent_view_attendance_post(request):
    subject_id = request.POST.get("subject")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    start_date_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    x = int(request.user.id) - 1
    #print(request.user.id,x)
    subject_obj = Subjects.objects.get(id=subject_id)
    user_obj = CustomUser.objects.get(id=str(x))
    stud_obj = Students.objects.get(user=user_obj)

    attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse),
                                           subject_id=subject_obj)
    attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)

    return render(request, "parent_template/parent_attendance_data.html", {"attendance_reports": attendance_reports})

def parent_view_result(request):
    x = int(request.user.id) - 1
    student = Students.objects.get(user=str(x))
    studentresult = StudentResult.objects.filter(student_id=student.id)
    return render(request, "parent_template/parent_result.html", {"studentresult": studentresult})

def parent_feedback(request):
    parent_id = Parents.objects.get(user=request.user.id)
    feedback_data = FeedBackParent.objects.filter(parent_id=parent_id)
    return render(request, "parent_template/parent_feedback.html", {"feedback_data": feedback_data})


def parent_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("parent_feedback"))
    else:
        feedback_msg = request.POST.get("feedback_msg")

        parent_obj = Parents.objects.get(user=request.user.id)
        try:
            feedback = FeedBackParent(parent_id=parent_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("parent_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("parent_feedback"))

def parent_all_notification(request):
    parent = Parents.objects.get(user=request.user.id)
    notifications = NotificationParent.objects.filter(parent_id=parent.id)
    return render(request, "parent_template/all_notification.html", {"notifications": notifications})

def parent_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    parent = Parents.objects.get(user=user)
    return render(request, "parent_template/parent_profile.html",
                  {"parent": parent})


def parent_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("parent_profile"))
    else:

        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            # customuser.first_name = first_name
            # customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            '''
            student = Students.objects.get(user=customuser)
            student.address = address
            student.dob = dob
            student.gender = gender
            student.ph_no = ph_no
            student.save()
            '''
            messages.success(request, "Successfully Updated Password")
            return HttpResponseRedirect(reverse("parent_profile"))
        except:
            messages.error(request, "Failed to Update Password")
            return HttpResponseRedirect(reverse("parent_profile"))