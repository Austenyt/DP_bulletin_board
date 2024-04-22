from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from board.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
            Форма для регистрации пользователя.

    """

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """
        Форма для редактирования пользователя.

    """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_not_blocked')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserAdminForm(StyleFormMixin, UserChangeForm):
    """
        Форма для редактирования зарегистрированных пользователей из-под админа.

    """
    class Meta:
        model = User
        fields = ['email', 'is_not_blocked']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
