import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views import generic

from learning.models import Booking, Lesson

#@TODO Enhance layout

class DashboardMainView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard/dashboard_main.html'


class DashboardBookingsListView(LoginRequiredMixin, generic.ListView):
    template_name = 'dashboard/dashboard_bookings.html'
    context_object_name = 'all_bookings'

    def get_queryset(self):
        bookings = Booking.objects.order_by('time_booked').all()
        if not (self.request.user.is_superuser or self.request.user.is_staff):
            bookings = Booking.objects.filter(student=self.request.user)
        return bookings

    def get_context_data(self, *, object_list=None, **kwargs):
        context =  super().get_context_data(object_list=object_list, **kwargs)
        context['pending_bookings'] = context['all_bookings'].filter(time_booked__gte=timezone.now() - datetime.timedelta(minutes=Booking.EXPIRY_MINUTE_TIME), status=Booking.PENDING)
        context['expired_bookings'] = context['all_bookings'].filter(time_booked__lt=timezone.now() - datetime.timedelta(minutes=Booking.EXPIRY_MINUTE_TIME), status=Booking.PENDING)
        context['accepted_bookings'] = context['all_bookings'].filter(status=Booking.ACCEPTED)
        context['rejected_bookings'] = context['all_bookings'].filter(status=Booking.REJECTED)
        context['cancelled_bookings'] = context['all_bookings'].filter(status=Booking.CANCELLED)
        return context


class DashboardHistoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'dashboard/dashboard_lesson_history.html'
    context_object_name = 'all_lessons'

    def get_queryset(self):
        lessons = Lesson.objects.order_by('time_start').all()
        if not (self.request.user.is_superuser or self.request.user.is_staff):
            if self.request.user.is_teacher:
                lessons = Lesson.objects.filter(teacher=self.request.user)
            else:
                lessons = Lesson.objects.filter(student=self.request.user)
        return lessons

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['current_lessons'] = context['all_lessons'].filter(time_end__gte=timezone.now())
        context['finished_lessons'] = context['all_lessons'].filter(time_end__lt=timezone.now())
        return context
