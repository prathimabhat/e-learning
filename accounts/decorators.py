from django.contrib.auth.decorators import login_required,user_passes_test


staff_login_required_=user_passes_test(lambda u: False if u.user_type == '1' or u.user_type == '3' else True)

def staff_login_required(view_func):
	decorated_view_func = login_required(staff_login_required_(view_func))
	return decorated_view_func

student_login_required_=user_passes_test(lambda u: False if u.user_type == '2' or u.user_type == '1' else True)

def student_login_required(view_func):
	decorated_view_func = login_required(student_login_required_(view_func))
	return decorated_view_func

admin_login_required_=user_passes_test(lambda u: False if u.user_type == '2' or u.user_type == '3' else True)

def admin_login_required(view_func):
	decorated_view_func = login_required(admin_login_required_(view_func))
	return decorated_view_func
'''
def is_admin(self):
    if str(self.user_type) == '1':
        return True
    else:
        return False
admin_login_required_ = user_passes_test(lambda u: True if u.is_admin else False)
def admin_login_required(view_func):
    decorated_view_func = login_required(admin_login_required_(view_func))
    return decorated_view_func

def is_staff(self):
    if str(self.user_type) == '2':
        return True
    else:
        return False
staff_login_required_ = user_passes_test(lambda u: True if u.is_staff else False)
def staff_login_required(view_func):
    decorated_view_func = login_required(staff_login_required_(view_func))
    return decorated_view_func

def is_student(self):
    if str(self.user_type) == '3':
        return True
    else:
        return False
student_login_required_ = user_passes_test(lambda u: True if u.is_student else False)
def student_login_required(view_func):
    decorated_view_func = login_required(student_login_required_(view_func))
    return decorated_view_func'''