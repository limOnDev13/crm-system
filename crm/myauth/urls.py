from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

app_name = "myauth"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page=reverse_lazy("myauth:login")),
        name="logout"
    ),
]
