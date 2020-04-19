from account.models import User
from django.shortcuts import render
from django.views import generic
from belajar_online import settings

# class IndexView(generic.DetailView):
#     template_name = 'main/index.html'

def index(request):
    return render(request, 'main/index.html', {
        'user': request.user,
        'nav': False,
        'footer': True,
        'dev_mode': settings.DEV_MODE
    })
