from django.urls import include, path
from .views import dashboard

urlpatterns = [
    path('user/', include('allauth.urls')),
    path("dashboard/", dashboard, name="dashboard"),
]
