import random

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


def user_directory_path(instance, filename):
    # Will be formatted as 'account/{id}_{username}/{salt}_{filename}'
    salt = random.randint(0, 99999)
    return f'account/{instance.user.id}_{instance.user.username}/{salt:05d}_{filename}'


def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('This field only accepts .pdf files.')


class User(AbstractUser):
    is_teacher = models.BooleanField('Teacher status', default=0,
                                     help_text='Designates whether the user have teacher access.')

    def __str__(self):
        return self.username


class UserDetail(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    phone_validator = RegexValidator(regex=r'0[\d]{9,12}',
                                     message='Phone number must start with 0. Up to 13 digits allowed.')

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(
        'Gender',
        max_length=1,
        choices=GENDER_CHOICES
    )
    date_of_birth = models.DateField('Date of Birth', null=True)
    address = models.CharField('Address', max_length=96)
    phone_number = models.CharField('Phone Number', validators=[phone_validator], max_length=13)
    ktp = models.ImageField('Identification ID (KTP/SIM/Student Card)', upload_to='account/document/ktp/%Y%m%d',
                            help_text='Only accepts images')
    occupation = models.CharField('Occupation', max_length=32)
    experiences = models.CharField('Experiences', max_length=32)
    cv = models.FileField('CV', upload_to='account/document/cv/%Y%m%d', validators=[validate_file_extension],
                           help_text='Only accepts pdfs')
    photos = models.ImageField('Photos', upload_to='account/photos/%Y%m%d', null=True, blank=True)
    about = models.CharField('About', max_length=1024, blank=True)

    def __str__(self):
        return 'Userdetail with user ' + str(self.user)
