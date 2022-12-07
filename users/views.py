from django.shortcuts import render


def dashboard(request):
    return render(request, template_name="users/dashboard.html")

