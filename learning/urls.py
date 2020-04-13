from django.urls import path

from . import views

app_name = 'learning'
urlpatterns = [
    path('schedule', views.ScheduleView.as_view(), name='schedule'),
    path('teachers/', views.TeacherListView.as_view(), name='list_teachers'),
]
