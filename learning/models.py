from django.db import models
from django.urls import reverse_lazy

from account.models import User


# def is_user_teacher(value):
#     if


class Course(models.Model):
    name = models.CharField('Name', max_length=24, unique=True)
    description = models.CharField('Description', max_length=96)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    #@TODO Add lesson model validation
    DAY_OF_WEEK_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Teacher', related_name='teacher_lessons')
    student = models.ManyToManyField(User, db_table='learning_attend_lesson', verbose_name='Student', related_name='student_lessons', blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    day_of_week = models.CharField(
        'Day of Week',
        max_length=3,
        default='MON',
        choices=DAY_OF_WEEK_CHOICES,
        null=True,
    )
    time = models.TimeField('Time', null=True)
    fee = models.IntegerField('Fee', default=0, blank=True)

    class Meta:
        unique_together = (('teacher', 'course', 'day_of_week', 'time'),)

    def get_absolute_url(self):
        return reverse_lazy('learning:detail_lesson', args=[self.pk])

    def __str__(self):
        return f'Lesson: {self.teacher} on {self.course}'
