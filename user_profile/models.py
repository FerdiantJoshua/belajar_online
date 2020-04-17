from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from account.models import User
from learning.models import Course


class TeacherPortfolio(models.Model):
    class GPAType(models.TextChoices):
        W = 'W', 'Weighted'
        UW = 'UW', 'Unweighted'

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Teacher', null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course', null=True,
                               help_text='You can only have one portfolio per course')
    score = models.DecimalField('Score', max_digits=3, decimal_places=2,
                                validators=[MinValueValidator(0), MaxValueValidator(5)])
    gpa_type = models.CharField('GPA Type', max_length=2, choices=GPAType.choices, default=GPAType.UW,
                                help_text='Maximum GPA 4.0 for "Weighted", and 5.0 for "Unweighted"')
    proof = models.ImageField('Experiences Proofs', upload_to='learning/teacher/proof/%Y%m%d', default='')

    def get_absolute_url(self):
        return reverse('user_profile:detail_portfolio', args=[self.teacher, self.pk])

    class Meta:
        unique_together = (('teacher', 'course'),)

    def __str__(self):
        return f'{self.teacher}\'s portfolio on course {self.course}'
