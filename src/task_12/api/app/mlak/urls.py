from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


app_name = "mlak"


urlpatterns = [
    path("", views.BooksView.as_view(), name="index"),
    path(
        "login/",
        LoginView.as_view(
            template_name="mlak/login.html",
            next_page="mlak:index",
            redirect_authenticated_user=True,
                ),
        name="login",
            ),
    path(
        "logout/",
        LogoutView.as_view(next_page="mlak:index"),
        name="logout",
            ),
    path(
        "signup/",
        views.SignUpView.as_view(),
        name="signup"
            ),
        ]
