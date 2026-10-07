from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from .forms import RegisterForm, LoginForm, ProfileForm
from .models import User


class RegisterView(CreateView):
    """Регистрация нового пользователя."""
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f'Добро пожаловать, {self.object.username}!')
        return response


class CustomLoginView(LoginView):
    """Вход по email."""
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


def logout_view(request):
    """Выход."""
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('accounts:login')


class ProfileView(LoginRequiredMixin, TemplateView):
    """Личный кабинет."""
    template_name = 'accounts/profile.html'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля."""
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль обновлён.')
        return super().form_valid(form)