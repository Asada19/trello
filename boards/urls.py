from django.urls import path, re_path

from .views import BoardListView, BoardCreateView, FavoriteView, BoardDetailView, BoardUpdateView, \
    BoardDeleteView, new_column, ColumnUpdateView, CardUpdateView, new_card, view_card, CardDetailView, \
    CardMarkCreateView, TitleChangeView, DescriptionChangeView, ChecklistCreateView, FileAddView, CardView, \
    CommentCreateView, SearchView

urlpatterns = [
    # Board
    path("", BoardListView.as_view(), name="board_index"),
    path("create", BoardCreateView.as_view(), name='board_create'),
    path("<int:pk>/", BoardDetailView.as_view(), name="board_detail"),
    path("<int:pk>/update", BoardUpdateView.as_view(), name='board_update'),
    path("<int:pk>/delete", BoardDeleteView.as_view(), name='board_delete'),
    path("favorite/<int:id>", FavoriteView.as_view(), name="favorite"),

    # Columns
    path('<int:pk>/new_column', new_column, name="new_column"),
    path('<int:pk>/delete_column/<int:column_id>/delete', ColumnUpdateView.delete, name="column_delete"),
    path('<int:pk>/update_column/<int:column_id>/update', ColumnUpdateView.as_view(), name="column_update"),

    # Cards crud
    path('new-card', new_card, name='card_create'),
    path('card/<int:pk>/', CardView.as_view(), name='card_detail'),
    path('card/<int:pk>/update/', CardUpdateView.as_view(), name='card_update'),
    path('card/<int:pk>/delete/', CardView.delete, name='card_delete'),
    path('drop/', CardView.drop, name='card_delete'),

    # Card details
    path("card/<int:pk>/mark/", CardMarkCreateView.as_view(), name="add_mark"),
    path('card/<int:pk>/file/', FileAddView.as_view(), name='add_file'),
    path('card/<int:pk>/checklist/', ChecklistCreateView.as_view(), name='add_checklist'),
    path("card/<int:pk>/comment/", CommentCreateView.as_view(), name="card-comment-add"),
    path("search/", SearchView.as_view(), name="search_results"),

    # path('card/<int:card_id>/title/', TitleChangeView.as_view(), name='card_update_title'),
    # path('card/<int:card_id>/description/', DescriptionChangeView.as_view(), name='card_update_description'),
    re_path(r'^cards/(?P<card_id>\d+)/', view_card),
]

