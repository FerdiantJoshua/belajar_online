from django.urls import path

from . import views

app_name = 'learning'
urlpatterns = [
    path('teachers/', views.TeacherListView.as_view(), name='list_teachers'),
    path('lessons/', views.LessonListView.as_view(), name='list_lessons'),
    path('lesson/<int:pk>', views.LessonDetailView.as_view(), name='detail_lesson'),
    path('lesson/book/', views.book_lesson, name='book_lesson'),
    path('lesson/create', views.LessonCreateView.as_view(), name='create_lesson'),
    path('lesson/edit/<int:pk>', views.LessonUpdateView.as_view(), name='edit_lesson'),
    path('lesson/delete/<int:pk>', views.LessonDeleteView.as_view(), name='delete_lesson'),
]
