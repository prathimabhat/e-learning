from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,SessionYearModel,AdminHOD,Parents,Staffs,Students,Courses
from student_management.models import Subjects,Attendance,AttendanceReport,FeedBackStudent,FeedBackStaffs,FeedBackParent,NotificationStudent,NotificationStaffs,NotificationParent,StudentResult,LeaveReportStudent,LeaveReportStaff
from forum.models import Questions,Answers
from assignments.models import Assignment,Submission,Quiz,QuizQuestions,QuizAnswers,QuizChoice
from notes.models import notes
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser)
admin.site.register(SessionYearModel)
admin.site.register(AdminHOD)
admin.site.register(Parents)
admin.site.register(Staffs)
admin.site.register(Students)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStudent)
admin.site.register(FeedBackStudent)
admin.site.register(NotificationStudent)
admin.site.register(StudentResult)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedBackStaffs)
admin.site.register(NotificationStaffs)
admin.site.register(FeedBackParent)
admin.site.register(NotificationParent)
admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(notes)
admin.site.register(Quiz)
admin.site.register(QuizQuestions)
admin.site.register(QuizAnswers)
admin.site.register(QuizChoice)