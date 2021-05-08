from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

'''class EmailBackEnd(ModelBackend):
    def authenticate(self,request,username=None,password=None,**kwargs):
        UserModel = get_user_model()
        if username is None:
            username=kwargs.get(UserModel.USERNAME_FIELD)
        try:
            case_insensitive_username_field='{}__iexact'.format(UserModel.USERNAME_FIELD)
            user=UserModel._default_manager.get(**{case_insensitive_username_field:username})
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

'''
class EmailBackEnd(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel=get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        
        else:
            if user.check_password(password):
                return user

    def get_user(self, user_id):
        user_model = get_user_model() 
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

  

