from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from .forms import RegistrationForms
from .models import User

class RegisterView(generic.FormView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegistrationForms
    success_url = '/'

    def form_valid(self, form):
        data = form.cleaned_data
        form.save(data)
        user = authenticate(self.request, username=data['username'], password=data['password'])
        login(self.request, user)
        return super().form_valid(form)


