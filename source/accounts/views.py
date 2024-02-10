from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import UserProfileForm

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile_edit.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile
