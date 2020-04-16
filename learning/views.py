from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from account.models import User
from belajar_online.utils import add_invalid_css_class_to_form
from .forms import LessonForm
from .models import Lesson, Course


#@TODO Finish this learning management views

class LessonListView(LoginRequiredMixin, generic.ListView):
    model = Lesson
    template_name = 'learning/lesson_list.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        course_name = self.request.GET.get('course')
        teacher_name = self.request.GET.get('teacher')
        if course_name or teacher_name:
            courses = Course.objects.filter(name__icontains=course_name)
            course_ids = [] if not courses else list(map(lambda x: x.get('pk'), courses.values('pk')))

            teachers = User.objects.filter(
                Q(first_name__icontains=teacher_name) |
                Q(username__icontains=teacher_name) |
                Q(last_name__icontains=teacher_name)
            )
            teacher_ids = [] if not teachers else list(map(lambda x: x.get('pk'), teachers.values('pk')))
            if bool(course_name) and bool(teacher_name):
                lessons = Lesson.objects.filter(Q(course__in=course_ids) & Q(teacher__in=teacher_ids))
            elif bool(course_name):
                lessons = Lesson.objects.filter(Q(course__in=course_ids))
            else:
                lessons = Lesson.objects.filter(Q(teacher__in=teacher_ids))
        else:
            lessons = Lesson.objects.all()
        return lessons

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form_init'] = {'course': self.request.GET.get('course'), 'teacher': self.request.GET.get('teacher')}
        return context


class LessonCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'learning/lesson_create_form.html'
    form_class = LessonForm

    def get_success_url(self):
        success_url = reverse('learning:list_lessons')
        return success_url

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

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
