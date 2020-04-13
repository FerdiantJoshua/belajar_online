from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from account.models import User
from belajar_online.utils import add_invalid_css_class_to_form
from .forms import LessonForm
from .models import Lesson

#@TODO Finish this learning management views

class LessonListView(LoginRequiredMixin, generic.ListView):
    model = Lesson
    template_name = 'learning/lesson_list.html'
    context_object_name = 'lessons'


class LessonCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'learning/lesson_create_form.html'
    form_class = LessonForm

    def get_success_url(self):
        success_url = reverse('learning:list_lesson')
        return success_url

    @add_invalid_css_class_to_form
    def form_invalid(self, form):
        return super().form_invalid(form)


class LessonDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lesson
    template_name = 'learning/lesson_detail.html'
    context_object_name = 'lesson'


class LessonUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Lesson
    template_name = 'learning/lesson_update_form.html'
    context_object_name = 'lesson'


class LessonDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Lesson
    template_name = 'learning/lesson_detail.html'
    context_object_name = 'lesson'


class TeacherListView(LoginRequiredMixin, generic.ListView):
    template_name = 'learning/teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        teachers = User.objects.filter(is_teacher=True)
        return teachers
