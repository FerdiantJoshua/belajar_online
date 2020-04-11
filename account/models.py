from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
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
    phone_validator = RegexValidator(regex=r'0[\d]{9,12}', message='Phone number must start with 0. Up to 13 digits allowed.')

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(
        'Gender',
        max_length=1,
        choices=GENDER_CHOICES
    )
    date_of_birth = models.DateField('Date of Birth', null=True)
    address = models.CharField('Address', max_length=96)
    phone_number = models.CharField('Phone Number', validators=[phone_validator], max_length=13)
    ktp = models.ImageField('Identification ID (KTP/SIM/Student Card)', upload_to='account/ktp/%Y%m%d')
    occupation = models.CharField('Occupation', max_length=32)
    experiences = models.CharField('Experiences', max_length=32)
    experiences_proofs = models.ImageField('Experiences Proofs', upload_to='account/proof/%Y%m%d')

    def __str__(self):
        return 'Userdetails with user ' + str(self.user)


class UserAppraisal(models.Model):
    RATING_CHOICE = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appraisal_target_user')
    source_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appraisal_source_user')
    rating = models.SmallIntegerField (
        'Rating',
        choices= RATING_CHOICE,
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ],
    )
    feedback = models.TextField('Feedback', blank=True)
    date = models.DateField('Date', null=True)

    class Meta:
        unique_together = (('target_user', 'source_user'), )

    def __str__(self):
        return f'Appraisal from user {self.source_user} -> user {self.target_user}: {self.rating}'

# up.id = UserAppraisal.objects.filter(target_user=u1, source_user=u2)[0].id
