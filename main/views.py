from account.models import User
from django.shortcuts import render
from django.views import generic
from belajar_online import settings
from django.template import RequestContext
from django.http import HttpResponse


class IndexView(generic.TemplateView):
    template_name = 'main/index.html'
