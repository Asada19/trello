from django.urls import include, re_path, path

from .views import dashboard, register

urlpatterns = [
    re_path(r"", include("django.contrib.auth.urls")),
    path("dashboard", dashboard, name="dashboard"),
    re_path(r"^oauth/", include("social_django.urls")),
    re_path(r"^register/", register, name="register"),
]
