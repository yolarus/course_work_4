from django.urls import path

from . import views
from .apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.LoginUserView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", views.LogoutUserView.as_view(), name="logout"),
    path("email-confirm/<str:token>/", views.email_verification, name="email-confirm"),
    path("users/update/<int:pk>/", views.UserUpdateView.as_view(), name="user_update"),
    path("users/detail/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("users/", views.UserListView.as_view(), name="user_list"),

    path("password-reset/", views.UserPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done", views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", views.UserPasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("password-reset/complete/", views.UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
