from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from .forms import RegistrationForm, LoginForm, UserDetailsForm
from .models import User, UserDetails


def add_invalid_css_class_to_form(func):
    def wrapper(*args, **kwargs):
        form = args[1]
        objects = form.fields if form.non_field_errors() else form.errors
        for key in objects:
            field = form.fields.get(key)
            field.widget.attrs.update({'class': field.widget.attrs['class'] + ' is-invalid'})
        return func(*args, **kwargs)
    return wrapper


class EnhancedLoginView(LoginView):
    model = User
    form_class = LoginForm
    success_url = 'account:user_details'
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
    success_url = reverse_lazy('account:user_details')

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
        UserDetails(user=user).save()
        login(self.request, user)
        return super().form_valid(form)

    @add_invalid_css_class_to_form
    def form_invalid(self, form):
        return super().form_invalid(form)


class UserDetailsView(LoginRequiredMixin, generic.FormView):
    # model = UserDetails
    template_name = 'account/user_details.html'
    form_class = UserDetailsForm
    success_url = reverse_lazy('account:user_details')
    login_url = 'account:login'
    # redirect_field_name = 'redirect_to'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            user_details = UserDetails.objects.get(pk=self.request.user)
        except:
            user_details = UserDetails(user=self.request.user)
            user_details.save()
        kwargs.update({'instance': user_details})
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_teacher:
            form.fields.pop('occupation')
            form.fields.pop('experiences')
            form.fields.pop('experiences_proofs')
        else:
            form.fields['occupation'].widget.attrs.update({'required':''})
            form.fields['experiences'].widget.attrs.update({'required':''})
            form.fields['experiences_proofs'].widget.attrs.update({'required':''})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    @add_invalid_css_class_to_form
    def form_invalid(self, form):
        return super().form_invalid(form)
