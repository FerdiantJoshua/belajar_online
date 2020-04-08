from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    is_teacher = models.BooleanField(default=0)
    def __str__(self):
        return self.username

class UserDetails(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
    )
    date_of_birth = models.DateField()
    address = models.CharField(max_length=96)
    phone_validator = RegexValidator(regex=r'0[\d]{9,12}', message='Phone number must start with 0. Up to 13 digits allowed.')
    phone_number = models.CharField(validators=[phone_validator], max_length=13)
    ktp = models.ImageField(upload_to='account/ktp/%Y%m%d')
    occupation = models.CharField(max_length=32, blank=True)
    experiences = models.CharField(max_length=32, blank=True)
    experiences_proofs = models.ImageField(upload_to='account/proof/%Y%m%d', blank=True)

    def __str__(self):
        return 'User with id ' + str(self.user)
