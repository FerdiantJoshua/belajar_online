from account.models import User
from django.shortcuts import render
from django.views import generic

# class IndexView(generic.DetailView):
#     template_name = 'main/index.html'

def index(request):
    return render(request, 'main/index.html', {'user': request.user})
