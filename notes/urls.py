from django.urls import path
import notes.views as views
app_name="notes"

urlpatterns=[

	path('',views.home,name="home"),
	path('<int:subject>/',views.detail,name="detail"),
	path('<int:subject>/upload/',views.upload_notes,name="upload_notes"),
	path('<int:subject>/write/',views.write_notes,name="write_notes"),
	path('<int:pk>/view_notes/',views.view_written_notes,name="view_notes"),
	path('<int:pk>/edit/',views.edit_notes,name="edit_notes"),
	path('<int:pk>/delete_upload/',views.delete_upload,name="delete_upload"),
	
]