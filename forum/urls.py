from django.urls import path
from forum import views

app_name='forum'
urlpatterns=[
	path('',views.SubjectView,name="SubjectView"),
	path('staff/',views.StaffSubjectView,name="staff_subject_view"),
	path('contact_instructor/',views.teacher_forum,name="contact_instructor"),
	path('contact_instructor/<int:pk>/',views.teacher_forum_questions,name="teacher_forum_questions"),
	path('contact_instructor/<int:pk>/new_question/',views.teacher_forum_new_question,name="teacher_forum_new_question"),

	path('my_questions/',views.MyQuestionsView.as_view(),name="my_questions"),
	path('my_answers/',views.MyAnswersView.as_view(),name="my_answers"),
	path('my_questions/<int:pk>/edit/',views.QuestionUpdateView,name="question_update"),
	path('my_answers/<int:pk>/edit/',views.AnswerUpdateView,name="answer_update"),
	path('my_questions/<int:pk>/delete/',views.QuestionDeleteView,name="question_delete"),
	path('my_answers/<int:pk>/delete/',views.AnswerDeleteView,name="answer_delete"),

	path('<str:subject>/',views.SubforumView,name="subforum"),
	path('staff/<str:subject>/',views.StaffSubforumView,name="staff_subforum"),
	path('<str:subjects>/questions/new/',views.NewQuestionView,name="new_question"),
	path('questions/<int:pk>/',views.QuestionView.as_view(),name="question-detail"),
	path('staff/questions/<int:pk>/',views.StaffQuestionView.as_view(),name="staff_question_detail"),
	path('questions/<int:pk>/answer/',views.AnswerView,name="answer-detail"),
	path('staff/questions/<int:pk>/answer/',views.StaffAnswerView,name="staff_new_answer"),
	path('up_vote/<int:pk>/',views.QuestionUpVoteView,name="up_vote"),
	path('down_vote/<int:pk>/',views.QuestionDownVoteView,name="down_vote"),
	path('answer_up_vote/<int:pk>/<int:pk_alt>',views.AnswerUpVoteView,name="answer_up_vote"),
	path('answer_down_vote/<int:pk>/<int:pk_alt>',views.AnswerDownVoteView,name="answer_down_vote"),
	path('report/<int:pk>',views.ReportView,name="report"),
	path('report/answer/<int:pk>/',views.ReportAnswerView,name="report_answer"),

	path('staff/my_answers/<int:pk>/edit/',views.StaffAnswerUpdateView,name="staff_answer_update"),
	path('staff/my_answers/<int:pk>/delete/',views.AnswerDeleteView,name="staff_answer_delete"),
	
]