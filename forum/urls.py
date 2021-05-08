from django.urls import path
from forum import views

urlpatterns=[
	path('<str:subjects>/questions/new/',views.NewQuestionView.as_view()),
	path('questions/<int:pk>/',views.QuestionView.as_view(),name="question-detail"),
	path('questions/<int:pk>/answer/',views.AnswerView.as_view(),name="answer-detail"),
	path('up_vote/<int:pk>/',views.QuestionUpVoteView,name="up_vote"),
	path('down_vote/<int:pk>/',views.QuestionDownVoteView,name="down_vote"),
	path('answer_up_vote/<int:pk>/<int:pk_alt>',views.AnswerUpVoteView,name="answer_up_vote"),
	path('answer_down_vote/<int:pk>/<int:pk_alt>',views.AnswerDownVoteView,name="answer_down_vote"),
	path('report/<int:pk>',views.ReportView,name="report"),
	path('report/answer/<int:pk>/',views.ReportAnswerView,name="report_answer")
]