from django import forms
from .models import User


class RegistrationForms(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        help_text='Your password must be 8-20 characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji.'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    def clean(self):
        cleaned_data =  super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']

        if password != confirm_password:
            err_message = 'Password and confirmation password is not equal!'
            self.add_error('password', err_message)
            self.add_error('confirm_password', err_message)

    # class Meta():
    #     model = User
    #     fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def save(self, data):
        User.objects.create_user(username=data['username'], email=data['email'], first_name=data['first_name'],
                                 last_name=data['last_name'], password=data['password'])
