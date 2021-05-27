
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.urls import path

app_name="assignments"
## @brief url patterns for the instructor app.
urlpatterns = [
	path('',views.assignment,name='assignment'),
    path('resource/',views.resource,name='resource'),

    path('student_assignment/',views.student_assignment,name='student_assignment'),
    path('student_resources/',views.student_resources,name='student_resources'),
    path('view_assignments/<int:pk>/',views.view_assignments,name='view_assignments'),
    path('upload_submission/<int:assignment_id>/',views.upload_submission,name='upload_submission'),
    path('view_resources/<int:course_id>/',views.view_resources,name='view_resources'),
	#path('select_subject/',views.select_subject,name="select_subject"),
    # url(r'^(?P<course_id>[0-9]+)/view_resources/$', views.view_resources, name='view_resources'),
	path('get_subject/',views.get_subject,name='get_subject'),
    path('get_subject_student/',views.get_subject_student,name='get_subject_student'),
    path('get_subject_resource/',views.get_subject_resource,name='get_subject_resource'),
    path('get_subject_student_resources/',views.get_subject_student_resources,name='get_subject_student_resources'),
    path('view_resources_staff/<int:pk>/',views.view_resources_staff,name='view_resources_staff'),
    url(r'^instructor_index/$', views.instructor_index, name='instructor_index'),
    url(r'^(?P<course_id>[0-9]+)/instructor_detail/$', views.instructor_detail, name='instructor_detail'),
    url(r'^(?P<course_id>[0-9]+)/detail/$', views.detail, name='detail'),
    url(r'^(?P<course_id>[0-9]+)/add_assignment/$', views.add_assignment, name='add_assignment'),
    url(r'^(?P<course_id>[0-9]+)/add_resource/$', views.add_resource, name='add_resource'),
    url(r'^(?P<course_id>[0-9]+)/add_notification/$', views.add_notification, name='add_notification'),
    url(r'^(?P<course_id>[0-9]+)/view_all_assignments/$', views.view_all_assignments, name='view_all_assignments'),
    url(r'^(?P<assignment_id>[0-9]+)/view_all_submissions/$', views.view_all_submissions, name='view_all_submissions'),
    url(r'^(?P<assignment_id>[0-9]+)/view_feedback/$', views.view_feedback, name='view_feedback'),
]