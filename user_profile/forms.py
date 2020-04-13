from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput

from belajar_online.utils import set_fields_css_class
from .models import TeacherPortfolio


class PortfolioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PortfolioForm, self).__init__(*args, **kwargs)
        set_fields_css_class(self.fields)

    def clean(self):
        is_course_exist = bool(self.cleaned_data.get('course'))
        if self.cleaned_data['gpa_type'] == TeacherPortfolio.GPAType.UW and self.cleaned_data['score'] > 4:
            error_msg = 'Unweighted GPA type only have 4.0 maximum value!'
            raise ValidationError({'score': error_msg, 'gpa_type': error_msg})
        elif is_course_exist and TeacherPortfolio.objects.filter(teacher=self.instance.teacher, course=self.cleaned_data['course']).first():
            error_msg = 'You have had a portfolio for this course! Please choose another course.'
            raise ValidationError({'course': error_msg})
        return super().clean()

    class Meta():
        model = TeacherPortfolio
        fields = '__all__'
        exclude = ['teacher']
