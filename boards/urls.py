from django.urls import path, re_path

from .views import BoardListView, BoardCreateView, FavoriteView, BoardDetailView, BoardUpdateView, \
    BoardDeleteView, new_column, ColumnUpdateView, CardUpdateView, new_card, view_card

urlpatterns = [
    path("", BoardListView.as_view(), name="board_index"),
    path("create/", BoardCreateView.as_view(), name='board_create'),
    path("favorite/<int:id>", FavoriteView.as_view(), name="favorite"),
    path("<int:pk>/", BoardDetailView.as_view(), name="board_detail"),
    path("<int:pk>/update/", BoardUpdateView.as_view(), name='board_update'),
    path("<int:pk>/delete/", BoardDeleteView.as_view(), name='board_delete'),
    path('<int:pk>/new-column/', new_column, name="new_column"),
    path('<int:pk>/delete_column/<int:column_id>/delete', ColumnUpdateView.delete, name="column_delete"),
    path('<int:pk>/update_column/<int:column_id>/update/', ColumnUpdateView.as_view(), name="column_update"),
    path('card/<int:card_id>/', CardUpdateView.as_view(), name='card_detail'),
    path('card/<int:card_id>/update/', CardUpdateView.as_view(), name='card_update'),
    path('card/<int:card_id>/delete/', CardUpdateView.delete, name='card_delete'),
    path('new-card/', new_card),
    re_path(r'^cards/(?P<card_id>\d+)/', view_card),
    path('drop/', CardUpdateView.drop),
]

