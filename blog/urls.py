from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", BlogListView.as_view(), name="blog_index"),
    path("<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),
    path("<category>/", BlogCategoryView.as_view(), name="blog_category")
]

