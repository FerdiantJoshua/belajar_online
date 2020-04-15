from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput, TimeInput
from django.utils import formats

from belajar_online.utils import set_fields_css_class
from .models import Lesson, Course


class LessonForm(ModelForm):
    #@TODO Create best form for lesson
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
            raise ValidationError({'time_start': error_msg})
        return super().clean()

    class Meta():
        model = Lesson
        fields = ['course', 'time_start', 'time_end', 'fee']
        # widgets = {
        #     'time_start': AdminDateWidget(),
        #     'time_end': AdminDateWidget(),
        # }
