from django.urls import path,include
from django.contrib.auth import views as auth_views
import accounts.views as views 
app_name="accounts"
urlpatterns = [
	path('login_request/',views.login_request,name="login_request"),
]