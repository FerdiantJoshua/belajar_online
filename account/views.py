from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from belajar_online.utils import add_invalid_css_class_to_form
from .forms import RegistrationForm, LoginForm
from .models import User


class EnhancedLoginView(LoginView):
    model = User
    form_class = LoginForm
    success_url = 'user_profile:profile'
    redirect_authenticated_user = True

    def __init__(self, *args, **kwargs):
        super(EnhancedLoginView, self).__init__(*args, **kwargs)

    @add_invalid_css_class_to_form
    def form_invalid(self, form):
        return super().form_invalid(form)


class RegisterView(generic.FormView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegistrationForm

    def get_success_url(self):
        success_url = reverse('user_profile:profile', args=[self.request.user.username])
        return success_url

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    @add_invalid_css_class_to_form
    def form_invalid(self, form):
        return super().form_invalid(form)
