from django.urls import include, path
from django.views.generic import TemplateView

from . import views

app_name = 'main'
urlpatterns = [
    # path('', TemplateView.as_view(template_name='main/index.html'), name='index'),
    path('', views.index, name='index'),
]
