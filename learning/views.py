from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _

from account.models import User
from belajar_online.utils import add_invalid_css_class_to_form
from .forms import LessonForm, BookingForm
from .models import Lesson, Course, Booking


class TeacherListView(LoginRequiredMixin, generic.ListView):
    template_name = 'learning/teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        teachers = User.objects.filter(is_teacher=True)
        return teachers


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
        self.lesson_count = lessons.count()
        return lessons

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_init_data'] = {'course': self.request.GET.get('course') or '',
                                       'teacher': self.request.GET.get('teacher') or ''}
        context['lesson_count'] = self.lesson_count
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
    success_url = reverse_lazy('learning:list_lessons')


@require_http_methods(['POST'])
@login_required
def book_lesson(request):
    if request.method == 'POST':
        form = BookingForm(request.user, request.POST)
        if form.is_valid():
            print('Uyeaa')
            form.instance.student = request.user
            booking = form.save()
            return redirect('learning:detail_booking', pk=booking.pk)
        else:
            print('Noooo')
            print(form.is_bound)
            print(form.errors)
            messages.error(request, form.errors['__all__'].as_text())
            return redirect('learning:list_lessons')


class BookingDetailView(LoginRequiredMixin, generic.edit.FormMixin, generic.DetailView):
    model = Booking
    template_name = 'learning/booking_detail.html'
    form_class = BookingForm
    context_object_name = 'booking'
    success_url = reverse_lazy('learning:list_lessons')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print(self.object.proof)
        kwargs.update({'user': self.request.user, 'instance': self.object})
        return kwargs

    def form_valid(self, form):
        message = _('Proof upload success! Please wait around 2 hours for our admins to review your booking.')
        print(message)
        form.instance.user = self.request.user
        form.save()
        messages.info(self.request, message)
        return super().form_valid(form)

    @add_invalid_css_class_to_form
    def form_invalid(self, form):
        print('Proof upload failed!')
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = context['booking'].lesson
        return context

#@TODO Fix permission
@require_http_methods(['POST'])
@login_required
def change_status(request, booking_id):
    if request.method == 'POST':
        status = request.POST['status']
        booking = get_object_or_404(Booking, pk=booking_id)
        booking.status = status
        if status == Booking.ACCEPTED:
            lesson = booking.lesson
            lesson.student.add(booking.student)
            lesson.student_count += 1
            lesson.save()
        booking.save()
    return redirect('learning:detail_booking', pk=booking_id)
