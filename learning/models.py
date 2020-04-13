from django.db import models

from account.models import User


class Course(models.Model):
    name = models.CharField('Name', max_length=24, unique=True)
    description = models.CharField('Description', max_length=96)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Teacher', related_name='lesson_teacher')
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Student', related_name='lesson_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    fee = models.IntegerField('Fee', default=0, blank=True)

    class Meta:
        unique_together = (('teacher', 'student', 'course'),)

    def __str__(self):
        return f'Lesson: {self.teacher} & {self.student} on {self.course}'


class Schedule(models.Model):
    DAY_OF_WEEK_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Lesson')
    day_of_week = models.CharField(
        'Day of Week',
        max_length=3,
        default='Monday',
        choices=DAY_OF_WEEK_CHOICES
    )
    time = models.TimeField('Time')

    class Meta:
        unique_together = (('lesson', 'day_of_week', 'time'),)
