from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, UserUpdateView, UserAdminUpdateView, UserListView, UserDetailView, UserDeleteView, \
    generate_new_password

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/profile/', UserUpdateView.as_view(), name='profile'),
    path('users/<int:pk>/edit/', UserAdminUpdateView.as_view(), name='user_update'),
    path('users', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/user_delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
]
