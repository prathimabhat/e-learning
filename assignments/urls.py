
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.urls import path

app_name="assignments"
## @brief url patterns for the instructor app.
urlpatterns = [
	path('',views.assignment,name='assignment'),
    path('resource/',views.resource,name='resource'),
    path('grade_view/<int:pk>/',views.gradeview,name="grade_view"),
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

    path('class_links/',views.get_class_links_staff,name="class_links"),
    path('class_links/new/',views.post_class_links,name="new_class_link"),
    path('students/class_links/',views.get_class_links_student,name="class_links_student"),

    path('quiz/',views.all_quizzes,name="all_quizzes"),

    path('quiz/new/',views.create_quiz,name="create_quiz"),
    path('quiz/<int:pk>/',views.get_quiz,name="get_quiz"),
    path('quiz/<int:pk>/question_type/',views.select_question_type,name="select_question_type"),
    path('quiz/<int:pk>/add_questions/',views.add_quiz_questions,name="add_quiz_questions"),
    path('quiz/<int:pk>/add_mcqs/',views.add_mcq_questions,name="add_mcq_questions"),
    path('quiz/<int:pk>/add_choices/',views.add_choices,name="add_choices"),
    path('quiz/<int:pk>/enable',views.enable_quiz,name="enable_quiz"),
    path('quiz/<int:pk>/disable',views.disable_quiz,name="disable_quiz"),
    path('quiz/all_submissions/<int:quiz_id>/',views.view_quiz_submissions,name="view_quiz_submissions"),
    path('quiz/submission_detail/<int:quiz_id>/<int:student_id>/',views.get_submission_detail,name="get_submission_detail"),
    path('student/quiz/',views.all_quizzes_students,name="all_quizzes_students"),
    path('student/quiz/<int:pk>/',views.get_quiz_students,name="get_quiz_students"),
    path('student/quiz/<int:quiz_id>/question/<int:question_id>/',views.quiz_question_detail,name="quiz_question_detail"),
    path('student/<int:quiz_id>/<int:question_id>/answer_save/',views.quiz_answer_save,name="quiz_answer_save"),

]