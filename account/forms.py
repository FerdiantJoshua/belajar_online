from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm, DateInput

from .models import User, UserDetails


def set_fields_css_class(fields, use_label=False):
    for key in fields:
        placeholder = ' '.join(list(map(lambda x: x[0].upper() + x[1:], key.split('_'))))
        if use_label:
            fields[key].label = placeholder
        fields[key].widget.attrs.update({'class': 'form-control', 'placeholder': placeholder})


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
    is_user_teacher = False

    def __init__(self, *args, **kwargs):
        super(UserDetailsForm, self).__init__(*args, **kwargs)
        set_fields_css_class(self.fields, use_label=True)
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['ktp'].label = 'Identification ID (KTP/SIM/Student Card)'
        self.fields['experiences'].label = 'Teaching Experiences'
        self.fields['experiences_proofs'].label = 'Teaching Experiences Proofs'

    class Meta():
        model = UserDetails
        fields = '__all__'
        exclude = ['user']
        # labels = {
        #     'date_of_birth': 'Date of Birth',
        #     'ktp': 'Identification ID (KTP/SIM/Student Card)',
        #     'experiences': 'Your Teaching Experiences',
        #     'experiences_proofs': 'Teaching Experiences Proofs',
        # }
        help_texts = {
            'ktp': 'Only accepts images',
            'experiences_proofs': 'Only accepts images',
        }
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
        }
