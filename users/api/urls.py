from django.urls import include, path
from .views import dashboard, LogoutView, LoginView, RegistrationAPIView, ActivationView

urlpatterns = [
    path('user/', include('allauth.urls')),
    path("dashboard/", dashboard, name="dashboard"),
    path('register/', RegistrationAPIView.as_view()),
    path('activate/<str:activation_code>', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
