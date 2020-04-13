from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from account.models import User
from belajar_online.utils import add_invalid_css_class_to_form
from learning.models import Schedule


class ScheduleView(LoginRequiredMixin, generic.ListView):
    model = Schedule
    template_name = 'learning/schedule.html'


class TeacherListView(LoginRequiredMixin, generic.ListView):
    template_name = 'learning/teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        teachers = User.objects.filter(is_teacher=True)
        return teachers
