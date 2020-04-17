from django.core.validators import MaxValueValidator, MinValueValidator
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
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Teacher', related_name='teacher_lessons')
    student = models.ManyToManyField(User, db_table='learning_attend_lesson', verbose_name='Student', related_name='student_lessons', blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    time_start = models.DateTimeField('Time Start', null=True)
    time_end = models.DateTimeField('Time End', null=True)
    fee = models.IntegerField('Fee', default=0, blank=True)
    student_count = models.PositiveSmallIntegerField('Total Student', default=0)
    max_students = models.PositiveSmallIntegerField('Maximum Students', default=3)
    is_cancelled = models.BooleanField('Is Cancelled', default=False, blank=True)

    class Meta:
        unique_together = (('teacher', 'time_start'),)

    def get_absolute_url(self):
        return reverse_lazy('learning:detail_lesson', args=[self.pk])

    def __str__(self):
        return f'Lesson: {self.teacher} on {self.course}'


class Booking(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Student')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Lesson')
    time_booked = models.DateTimeField('Time Booked', auto_now_add=True, null=True, blank=False)
    is_active = models.BooleanField('Is Active', default=0)

    def __str__(self):
        return f'Booking: {self.student} on {self.lesson}'


class UserAppraisal(models.Model):
    RATING_CHOICE = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    target_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    source_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_appraisal')
    rating = models.SmallIntegerField (
        'Rating',
        choices= RATING_CHOICE,
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ],
    )
    feedback = models.CharField('Feedback', max_length=256, blank=True)
    date = models.DateField('Date', null=True)

    class Meta:
        unique_together = (('target_lesson', 'source_user'), )

    def __str__(self):
        return f'Appraisal: user {self.source_user} -> lesson {self.target_lesson}: {self.rating}'

# up.id = UserAppraisal.objects.filter(target_user=u1, source_user=u2)[0].id
