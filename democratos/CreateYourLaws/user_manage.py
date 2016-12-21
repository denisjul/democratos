from registration.backends.default.views import RegistrationView
from CreateYourLaws.forms import Create_CYL_UserForm
from CreateYourLaws.models import CYL_user


class Create_User(RegistrationView):
    form_class = Create_CYL_UserForm

    def register(self, request, form_class):
        new_user = super(Create_User, self).register(request, form_class)
        user_profile = CYL_user()
        user_profile.user = new_user
        user_profile.field = form_class.cleaned_data['field']
        user_profile.save()
        return user_profile
