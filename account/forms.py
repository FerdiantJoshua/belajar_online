from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm, DateInput, Textarea

from belajar_online.utils import set_fields_css_class
from .models import User, UserDetail


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        set_fields_css_class(self.fields)


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        set_fields_css_class(self.fields)
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Password Confirmation'})

    def save(self, commit=True):
        user = super().save(commit)
        if not UserDetail.objects.filter(pk=user.pk):
            UserDetail(user=user).save()
        return user

    class Meta():
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class UserDetailPhotoForm(ModelForm):
    class Meta():
        model = UserDetail
        fields = ['photos']


class UserDetailForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserDetailForm, self).__init__(*args, **kwargs)
        set_fields_css_class(self.fields)

    class Meta():
        model = UserDetail
        fields = '__all__'
        exclude = ['user', 'photos']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
            'about': Textarea(),
        }
