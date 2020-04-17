from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic
from django.views.decorators.http import require_http_methods

from account.models import User
from belajar_online.utils import add_invalid_css_class_to_form
from .forms import LessonForm, BookingForm
from .models import Lesson, Course, Booking


#@TODO Finish this learning management views
class LessonListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 10
    model = Lesson
    template_name = 'learning/lesson_list.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        lessons = Lesson.objects.order_by('time_start').filter(time_end__gte=timezone.now(), is_cancelled=False)
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
                lessons = lessons.filter(Q(course__in=course_ids) & Q(teacher__in=teacher_ids))
            elif bool(course_name):
                lessons = lessons.filter(Q(course__in=course_ids))
            else:
                lessons = lessons.filter(Q(teacher__in=teacher_ids))
        return lessons

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_init_data'] = {'course': self.request.GET.get('course') or '',
                                       'teacher': self.request.GET.get('teacher') or ''}
        return context


@require_http_methods(['POST'])
@login_required
def book_lesson(request):
    if request.method == 'POST':
        form = BookingForm(request.user, request.POST)
        if form.is_valid():
            print('Uyeaa')
            lesson = Lesson.objects.get(pk=request.POST['lesson'])
            lesson.student_count += 1
            lesson.save()
            form.instance.student = request.user
            form.save()
        else:
            print('Noooo')
            print(form.is_bound)
            print(form.errors)
            messages.error(request, form.errors['__all__'].as_text())
            pass
    return redirect('learning:list_lessons')


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
    success_url = reverse_lazy('learning:list_lessons')


class TeacherListView(LoginRequiredMixin, generic.ListView):
    template_name = 'learning/teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        teachers = User.objects.filter(is_teacher=True)
        return teachers
