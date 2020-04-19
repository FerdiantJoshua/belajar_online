from django.urls import include, path
from django.views.generic import TemplateView

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
