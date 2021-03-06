import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput, TimeInput
from django.utils import formats, timezone
from django.utils.translation import gettext_lazy as _

from belajar_online.utils import set_fields_css_class
from .models import Lesson, Course, Booking


class LessonForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        set_fields_css_class(self.fields)
        self.user = user
        date_format = ['%Y/%m/%d %H:%M']
        self.fields['time_start'].input_formats = date_format
        self.fields['time_end'].input_formats = date_format

        teacher_portfolios = user.teacherportfolio_set.all()
        allowed_courses = list(map(lambda x: x['course'], teacher_portfolios.values('course')))
        self.fields['course'].queryset = Course.objects.filter(pk__in=allowed_courses)

    def clean(self):
        if Lesson.objects.filter(teacher=self.user, time_start=self.cleaned_data['time_start']):
            error_msg = 'You have already held a lesson at that time! Please pick another time.'
            raise ValidationError(_(error_msg), code='clash_lesson_schedule')
        elif self.cleaned_data['time_start'] >= self.cleaned_data['time_end']:
            error_msg = 'Your lesson\'s start time is earlier then it\'s end time!'
            raise ValidationError({'time_start': _(error_msg), 'time_end': _(error_msg)}, code='incorrect_time')
        return super().clean()

    class Meta():
        model = Lesson
        fields = ['course', 'time_start', 'time_end', 'fee', 'student_count']


class BookingForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        set_fields_css_class(self.fields)
        self.user = user
        try:
            self.is_creating_new = self.instance.student is None
        except:
            self.is_creating_new = True
        if self.is_creating_new:
            del self.fields['proof']
        else:
            del self.fields['lesson']
        print('This booking form has fields:', self.fields)

    def clean(self):
        print(timezone.now() - datetime.timedelta(minutes=Booking.EXPIRY_MINUTE_TIME))
        if self.user.is_teacher:
            error_msg = 'Teachers are not permitted to book a lesson!'
            raise ValidationError(_(error_msg), code='teacher_booking')
        if self.is_creating_new:
            lesson = self.cleaned_data['lesson']
            if Booking.objects.filter(student=self.user, lesson=lesson, time_booked__gt=timezone.now() - datetime.timedelta(minutes=Booking.EXPIRY_MINUTE_TIME), status=Booking.PENDING):
                error_msg = 'You are currently booking this lesson! Please cancel or complete the booking first.'
                raise ValidationError(_(error_msg), code='repetitive_booking')
            elif self.user.student_lessons.filter(pk=lesson.pk):
                error_msg = 'You have already been in this lesson!'
                raise ValidationError(_(error_msg), code='invalid_booking')
            elif lesson.student_count >= lesson.max_students:
                error_msg = 'Lesson is full!'
                raise ValidationError(_(error_msg), code='full_lesson')
            elif lesson.time_end < timezone.now():
                error_msg = 'This lesson has ended.'
                raise ValidationError(_(error_msg), code='finished_lesson')
        else:
            if self.instance.is_booking_expired():
                error_msg = 'Your booking is expired, please make another booking.'
                raise ValidationError({'proof': _(error_msg)}, code='expired_booking')
        return super().clean()

    class Meta():
        model = Booking
        fields = ['lesson', 'proof']
