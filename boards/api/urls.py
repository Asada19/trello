from django.urls import path, include
from .views import BoardAPIView, BoardDetailView, ColumnAPIView, ColumnDetailView, CardAPIView, CardDetailView, \
    MarkAPIView, MarkDetailView, CommentAPIView, CommentDetailView, FileAPIView, FileDetailView, ChecklistAPIView, \
    ChecklistDetailView

urlpatterns = [
    # user
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    # board
    path('board/', BoardAPIView.as_view(), name='boards'),
    path('board/<int:pk>', BoardDetailView.as_view(), name='board-details'),
    path('board/<int:pk>/columns', ColumnAPIView.as_view(), name='board-columns'),
    path('column/<int:column_id>', ColumnDetailView.as_view(), name='column-detail'),
    path('column/<int:column_id>/cards', CardAPIView.as_view(), name='column-cards'),

    # cards
    path('card/<int:card_id>', CardDetailView.as_view(), name='card-detail'),
    path('card/<int:card_id>/marks', MarkAPIView.as_view(), name='card-marks'),
    path('card/<int:card_id>/comments', CommentAPIView.as_view(), name='card-comments'),
    path('card/<int:card_id>/files', FileAPIView.as_view(), name='card-files'),
    path('card/<int:card_id>/check_list', ChecklistAPIView.as_view(), name='card-check_list'),

    # card details
    path('mark/<int:mark_id>', MarkDetailView.as_view(), name='mark-detail'),
    path('comment/<int:comment_id>', CommentDetailView.as_view(), name='comment-detail'),
    path('file/<int:file_id>', FileDetailView.as_view(), name='file-detail'),
    path('check_list/<int:check_id>', ChecklistDetailView.as_view(), name='check_list-detail'),

]
