from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm, DateInput

from belajar_online.utils import set_fields_css_class
from .models import User, UserDetails


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
        if not UserDetails.objects.filter(pk=user.pk):
            UserDetails(user=user).save()
        return user

    class Meta():
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class UserDetailsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserDetailsForm, self).__init__(*args, **kwargs)
        set_fields_css_class(self.fields)

    class Meta():
        model = UserDetails
        fields = '__all__'
        exclude = ['user']
        help_texts = {
            'ktp': 'Only accepts images',
            'experiences_proofs': 'Only accepts images',
        }
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
        }
