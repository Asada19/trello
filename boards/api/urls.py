from django.urls import path, include
from .views import BoardAPIView, BoardDetailView, ColumnAPIView, ColumnDetailView, CardAPIView, CardDetailView

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('board/', BoardAPIView.as_view(), name='boards'),
    path('board/<int:pk>', BoardDetailView.as_view(), name='board-details'),
    path('board/<int:pk>/columns', ColumnAPIView.as_view(), name='board-columns'),
    path('column/<int:column_id>', ColumnDetailView.as_view(), name='column-detail'),
    path('column/<int:column_id>/cards', CardAPIView.as_view(), name='column-cards'),
    path('card/<int:card_id>', CardDetailView.as_view(), name='card-detail'),
]
