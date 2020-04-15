from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from account.forms import UserDetailForm
from account.models import UserDetail, User
from .forms import PortfolioForm
from .models import TeacherPortfolio
from belajar_online.utils import add_invalid_css_class_to_form


class ProfileEdit(generic.FormView):
    # model = UserDetail
    template_name = 'user_profile/profile.html'
    form_class = UserDetailForm
    success_url = reverse_lazy('user_profile:profile')


class ProfileView(LoginRequiredMixin, generic.edit.FormMixin, generic.DetailView):
    #@TODO Enable edit and add photo feature
    login_url = 'account:login'

    model = User
    template_name = 'user_profile/profile.html'
    form_class = UserDetailForm
    context_object_name = 'user_owner'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        success_url = reverse('user_profile:profile', args=[self.user_owner])
        return success_url

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            user_details = UserDetail.objects.get(pk=self.user_owner)
        except:
            user_details = UserDetail(user=self.user_owner)
            user_details.save()
        kwargs.update({'instance': user_details})
        return kwargs

    def get_form(self, form_class=None):
        self.user_owner = get_object_or_404(User, username=self.kwargs['username'])
        form = super().get_form(form_class)
        if not self.user_owner.is_teacher:
            form.fields.pop('occupation')
            form.fields.pop('experiences')
            form.fields.pop('cv')
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_self_owned'] = self.user_owner == self.request.user
        if context['is_self_owned']:
            context['need_edit'] = bool(context['form'].errors) or not context['form'].instance.ktp
        context['appraisals'] = self.user_owner.appraisal_target_user.order_by('-date').all()
        context['portfolios'] = TeacherPortfolio.objects.filter(teacher=self.user_owner)
        return context

    def form_valid(self, form):
        form.instance.user = self.user_owner
        form.save()
        return super().form_valid(form)

    @add_invalid_css_class_to_form
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class PortfolioCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'user_profile/portfolio_create_form.html'
    form_class = PortfolioForm

    def get_success_url(self):
        success_url = reverse('user_profile:profile', args=[self.request.user.username])
        return success_url

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.teacher = self.request.user
        return form

    @add_invalid_css_class_to_form
    def form_invalid(self, form):
        return super().form_invalid(form)


class PortfolioDetailView(LoginRequiredMixin, generic.DetailView):
    model = TeacherPortfolio
    template_name = 'user_profile/portfolio_detail.html'
    context_object_name = 'portfolio'


class PortfolioUpdateView(LoginRequiredMixin, generic.UpdateView):
    #@TODO Manage permissions
    model = TeacherPortfolio
    fields = ['score', 'gpa_type', 'proof']
    template_name = 'user_profile/portfolio_update_form.html'
    context_object_name = 'portfolio'

    def get_success_url(self):
        success_url = reverse('user_profile:profile', args=[self.request.user.username])
        return success_url

    @add_invalid_css_class_to_form
    def form_invalid(self, form):
        return super().form_invalid(form)


class PortfolioDeleteView(LoginRequiredMixin, generic.DeleteView):
    #@TODO Manage permissions
    model = TeacherPortfolio
    template_name = 'user_profile/portfolio_detail.html'

    def get_success_url(self):
        success_url = reverse('user_profile:profile', args=[self.request.user.username])
        return success_url
