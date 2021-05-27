"""e_learning_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from e_learning_platform import settings
#import accounts.views as views 
import student_management.views as views
urlpatterns = [
	

	
    path('',include('django.contrib.auth.urls')), 

	path('accounts/',include('accounts.urls')),  

    path('admin/', admin.site.urls),
    path('reset_password/',
	auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html",email_template_name = 'accounts/password_reset_email.html'),
	name="password_reset"),

    path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
    name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
    name="password_reset_confirm"),

    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
    name="password_reset_complete"),

    path('assignments/',include('assignments.urls')),





    path('admin_home', views.admin_home, name="admin_home"),
    path('add_staff', views.add_staff, name="add_staff"),
    path('add_staff_save', views.add_staff_save, name="add_staff_save"),
    path('add_course', views.add_course, name="add_course"),
    path('add_course_save', views.add_course_save, name="add_course_save"),
    path('add_student', views.add_student, name="add_student"),
    path('add_student_save', views.add_student_save, name="add_student_save"),
    path('add_subject', views.add_subject, name="add_subject"),
    path('add_subject_save', views.add_subject_save, name="add_subject_save"),
    path('manage_staff', views.manage_staff, name="manage_staff"),
    path('manage_student', views.manage_student, name="manage_student"),
    path('manage_course', views.manage_course, name="manage_course"),
    path('manage_subject', views.manage_subject, name="manage_subject"),
    path('edit_staff/<str:staff_id>', views.edit_staff, name="edit_staff"),
    path('edit_staff_save', views.edit_staff_save, name="edit_staff_save"),
    path('edit_student/<str:student_id>', views.edit_student, name="edit_student"),
    path('select_student_class', views.select_student_class, name="select_student_class"),
    path('select_attendance_class', views.select_attendance_class, name="select_attendance_class"),
    path('select_subject', views.select_subject, name="select_subject"),
    path('edit_student_save', views.edit_student_save, name="edit_student_save"),
    path('edit_subject/<str:subject_id>', views.edit_subject, name="edit_subject"),
    path('edit_subject_save', views.edit_subject_save, name="edit_subject_save"),
    path('edit_course/<str:course_id>', views.edit_course, name="edit_course"),
    path('edit_course_save', views.edit_course_save, name="edit_course_save"),
    path('manage_session', views.manage_session, name="manage_session"),
    path('add_session_save', views.add_session_save, name="add_session_save"),
    path('check_email_exist', views.check_email_exist, name="check_email_exist"),
    path('check_parent_email_exist', views.check_parent_email_exist, name="check_parent_email_exist"),
    path('check_roll_number_exist', views.check_roll_number_exist, name="check_roll_number_exist"),
    #path('check_parent_roll_number_exist', HodViews.check_parent_roll_number_exist, name="check_parent_roll_number_exist"),
    path('check_teacher_roll_number_exist', views.check_teacher_roll_number_exist, name="check_teacher_roll_number_exist"),
    path('check_username_exist', views.check_username_exist, name="check_username_exist"),
    path('check_parent_username_exist', views.check_parent_username_exist, name="check_parent_username_exist"),
    path('student_feedback_message', views.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_replied', views.student_feedback_message_replied, name="student_feedback_message_replied"),
    path('staff_feedback_message', views.staff_feedback_message, name="staff_feedback_message"),
    path('staff_feedback_message_replied', views.staff_feedback_message_replied, name="staff_feedback_message_replied"),
    path('parent_feedback_message', views.parent_feedback_message, name="parent_feedback_message"),
    path('parent_feedback_message_replied', views.parent_feedback_message_replied,name="parent_feedback_message_replied"),
    path('student_leave_view', views.student_leave_view, name="student_leave_view"),
    path('staff_leave_view', views.staff_leave_view, name="staff_leave_view"),
    path('student_approve_leave/<str:leave_id>', views.student_approve_leave, name="student_approve_leave"),
    path('student_disapprove_leave/<str:leave_id>', views.student_disapprove_leave, name="student_disapprove_leave"),
    path('staff_disapprove_leave/<str:leave_id>', views.staff_disapprove_leave, name="staff_disapprove_leave"),
    path('staff_approve_leave/<str:leave_id>', views.staff_approve_leave, name="staff_approve_leave"),
    path('admin_view_attendance', views.admin_view_attendance, name="admin_view_attendance"),
    path('admin_get_attendance_dates', views.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    path('admin_get_attendance_student', views.admin_get_attendance_student, name="admin_get_attendance_student"),
    path('admin_profile', views.admin_profile, name="admin_profile"),
    path('admin_profile_save', views.admin_profile_save, name="admin_profile_save"),
    path('admin_send_notification_staff', views.admin_send_notification_staff, name="admin_send_notification_staff"),
    path('send_staff_notification', views.send_staff_notification, name="send_staff_notification"),
    path('send_student_notification', views.send_student_notification, name="send_student_notification"),
    path('admin_send_notification_student', views.admin_send_notification_student, name="admin_send_notification_student"),
    path('delete_student/<str:student_id>', views.delete_student, name="delete_student"),
    path('delete_staff/<str:staff_id>', views.delete_staff, name="delete_staff"),
    path('delete_course/<str:course_id>', views.delete_course, name="delete_course"),
    path('delete_subject/<str:subject_id>', views.delete_subject, name="delete_subject"),



    #Staff url path
    path('staff_home', views.staff_home, name="staff_home"),
    path('staff_take_attendance', views.staff_take_attendance, name="staff_take_attendance"),
    path('staff_update_attendance', views.staff_update_attendance, name="staff_update_attendance"),
    path('get_students',views.get_students, name="get_students"),
    path('save_attendance_data', views.save_attendance_data, name="save_attendance_data"),
    path('get_attendance_dates', views.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student', views.get_attendance_student, name="get_attendance_student"),
    path('save_updateattendance_data', views.save_updateattendance_data, name="save_updateattendance_data"),
    path('staff_apply_leave', views.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save', views.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback', views.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save', views.staff_feedback_save, name="staff_feedback_save"),
    path('staff_profile', views.staff_profile, name="staff_profile"),
    path('staff_profile_save', views.staff_profile_save, name="staff_profile_save"),
    path('staff_fcmtoken_save', views.staff_fcmtoken_save, name="staff_fcmtoken_save"),
    path('staff_all_notification', views.staff_all_notification, name="staff_all_notification"),
    path('staff_add_result', views.staff_add_result, name="staff_add_result"),
    path('save_student_result', views.save_student_result, name="save_student_result"),
    path('fetch_result_student', views.fetch_result_student, name="fetch_result_student"),
    path('select_class', views.select_class, name="select_class"),
    path('edit_select_class', views.edit_select_class, name="edit_select_class"),
    path('edit_result_select_class_session', views.edit_result_select_class_session, name="edit_result_select_class_session"),
    path('manage_student_result_list_display', views.manage_student_result_list_display, name="manage_student_result_list_display"),
    path('edit_student_result/<str:student_id>', views.edit_student_result, name="edit_student_result"),
    path('edit_student_result_save', views.edit_student_result_save, name="edit_student_result_save"),
    #path('manage_student_result', StaffViews.manage_student_result, name="manage_student_result"),
    #path('select_result_class', StaffViews.select_result_class, name="select_result_class"),
    #path('edit_manage_student_result_save', StaffViews.edit_manage_student_result_save, name="edit_manage_student_result_save"),


    #Student url path
    path('student_home', views.student_home, name="student_home"),
    path('student_view_attendance',views.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', views.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave', views.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save', views.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback', views.student_feedback, name="student_feedback"),
    path('student_feedback_save', views.student_feedback_save, name="student_feedback_save"),
    path('student_profile', views.student_profile, name="student_profile"),
    path('student_profile_save', views.student_profile_save, name="student_profile_save"),
    path('student_fcmtoken_save', views.student_fcmtoken_save, name="student_fcmtoken_save"),
    #path('firebase-messaging-sw.js', views.showFirebaseJS, name="show_firebase_js"),
    path('student_all_notification', views.student_all_notification, name="student_all_notification"),
    path('student_view_result', views.student_view_result,name="student_view_result"),


    path('parent_view_result', views.parent_view_result,name="parent_view_result"),
    path('parent_home', views.parent_home, name="parent_home"),
    path('parent_view_attendance', views.parent_view_attendance, name="parent_view_attendance"),
    path('parentent_view_attendance_post', views.parent_view_attendance_post, name="parent_view_attendance_post"),
    path('parent_feedback', views.parent_feedback, name="parent_feedback"),
    path('parent_feedback_save', views.parent_feedback_save, name="parent_feedback_save"),
    path('parent_all_notification', views.parent_all_notification, name="parent_all_notification"),
    path('admin_send_notification_parent', views.admin_send_notification_parent, name="admin_send_notification_parent"),
    path('send_parent_notification', views.send_parent_notification, name="send_parent_notification"),
    path('parent_profile', views.parent_profile, name="parent_profile"),
    path('parent_profile_save', views.parent_profile_save, name="parent_profile_save"),

    #forum urls
    path('forum/',include('forum.urls')),

    path('notes/',include('notes.urls')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



