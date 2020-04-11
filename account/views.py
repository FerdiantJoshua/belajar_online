from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from belajar_online.utils import add_invalid_css_class_to_form
from .forms import RegistrationForm, LoginForm, UserDetailsForm
from .models import User, UserDetails


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
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['need_edit'] = bool(context['form'].errors) or not context['form'].instance.ktp
        context['appraisals'] = self.request.user.appraisal_target_user.order_by('-date').all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    @add_invalid_css_class_to_form
    def form_invalid(self, form):
        return super().form_invalid(form)
