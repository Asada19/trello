from django.urls import path, re_path, reverse
from . import views
from .views import *

urlpatterns = [
    path("", BoardListView.as_view(), name="board_index"),
    path("favorite/", FavoriteView.as_view(), name="favorite"),
    path("create/", BoardCreateView.as_view(), name='board_create'),
    path("<int:pk>/", BoardDetailView.as_view(), name="board_detail"),
    path("<int:pk>/update/", BoardUpdateView.as_view(), name='board_update'),
    path("<int:pk>/delete/", BoardDeleteView.as_view(), name='board_delete'),
    path('<int:pk>/new-column/', new_column, name="new_column"),
    path('<int:pk>/delete_column/', ColumnDeleteView.as_view(), name="column_delete"),
    path('<int:pk>/update_column/', ColumnUpdateView.as_view(), name="column_update"),
    # path('card/<int:id>/update/', CardUpdateView.as_view(), name='card_update'),
    path('card/<int:card_id>/update/', update_card, name='card_update'),
    path('card/<int:card_id>/delete/', delete_card, name='card_delete'),
    path('new-card/', new_card),
    re_path(r'^cards/(?P<card_id>\d+)/', view_card),
    # path('card/<int:card_id>/delete/', CardDeleteView.as_view(), name='card_delete'),
    path('drop/', drop),
]

