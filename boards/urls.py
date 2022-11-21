from django.urls import path, re_path
from . import views
from .views import *

urlpatterns = [
    path("", BoardListView.as_view(), name="board_index"),
    path("create/", BoardCreateView.as_view(), name='board_create'),
    path("<int:pk>/", BoardDetailView.as_view(), name="board_detail"),
    path('<int:pk>/new-column/', new_column, name="new_column"),
    path('new-card/', new_card),
    re_path(r'^cards/(?P<card_id>\d+)/', view_card),
    path('drop/', drop),
]

