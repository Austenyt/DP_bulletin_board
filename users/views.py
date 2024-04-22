import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from config import settings
from users.forms import UserProfileForm, UserRegisterForm, UserAdminForm
from users.models import User


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
       Представление списка пользователей.

    """
    model = User
    extra_context = {
        'title': 'Пользователи'
    }
    permission_required = 'user.can_view_user_list'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_not_blocked=True)
        return queryset


class RegisterView(CreateView):
    """
       Представление регистрации нового пользователя.

    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject='Поздравляем с регистрацией',
            message='Вы зарегистрировались на нашей платформе, добро пожаловать!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
       Представление обновления профиля пользователя.

    """

    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    permission_required = 'user.can_block_user'

    def get_object(self, queryset=None):
        return self.request.user


class UserAdminUpdateView(LoginRequiredMixin, UpdateView):
    """
        Представление обновления профиля пользователя администратором.

    """
    model = User
    form_class = UserAdminForm
    success_url = reverse_lazy('users:user_list')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.kwargs['pk'])


class UserDetailView(LoginRequiredMixin, DetailView):
    """
        Представление просмотра профиля пользователя.

    """
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'
    extra_context = {
        'title': 'Карточка пользователя'
    }


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
        Представление удаления профиля пользователя.

    """
    model = User
    success_url = reverse_lazy('users:user_list')


@login_required
def generate_new_password(request):
    """
        Генерация нового пароля для пользователя.

    """
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('board:index'))
