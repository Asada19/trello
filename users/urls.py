from django.urls import include, re_path, path

from .views import dashboard, register

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("dashboard", dashboard, name="dashboard"),
    path("oauth/", include("social_django.urls")),
    path("register/", register, name="register"),
]
