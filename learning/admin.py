from django.contrib import admin

from .models import Course, Schedule, Lesson


class ScheduleInLine(admin.StackedInline):
    model = Schedule
    extra = 1
    min_num = 0


class LessonAdmin(admin.ModelAdmin):
    inlines = [ScheduleInLine]


admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
