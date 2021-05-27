from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserModel
from django.forms import forms

User = get_user_model()


class RegisterForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email',)
        field_classes = {'username': UsernameField}


class ProfileEditForm(forms.BaseForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'address', 'year_birth', 'phone_no', 'bank_no')


class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        field_classes = {'username': UsernameField}
        # widgets = {
        #
        # }
