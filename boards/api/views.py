import datetime
from django.shortcuts import get_object_or_404
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BoardSerializer, BoardDetailSerializer, ColumnSerializer, CardSerializer, MarkSerializer, \
    CommentSerializer, FileSerializer, ChecklistSerializer, FavoriteSerializer, MemberSerializer
from ..models import Board, Column, Card, Mark, Comment, File, Checklist, Favorite, Member
from ..permissions import IsBoardOwner


class BoardAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_class = [IsAuthenticated, IsBoardOwner]
    filter_backends = [filters.SearchFilter]
    search_filters = ['title', 'owner']

    @swagger_auto_schema(operation_summary='List all Board Objects')
    def get(self, request):
        boards = Board.objects.filter(owner=[request.user.id][0])
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BoardSerializer, operation_summary='Creates a new Board Object')
    def post(self, request):
        data = request.data
        serializer = BoardSerializer(data=data)
        if serializer.is_valid():
            board = serializer.save()
            board.owner = request.user
            board.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDetailView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsBoardOwner]

    def get_object(self, pk):
        return Board.objects.get(pk=pk)

    @swagger_auto_schema(operation_summary="get board object")
    def get(self, request, pk):
        board = self.get_object(pk)
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=BoardDetailSerializer, operation_summary="update method")
    def patch(self, request, pk):
        board = self.get_object(pk)
        serializer = BoardDetailSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('success!', status=status.HTTP_201_CREATED)
        return Response('bad request', status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="delete method")
    def delete(self, request, pk):
        board = self.get_object(pk)
        if board:
            board.delete()
            return Response('Board successfully deleted', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Board not found', status=status.HTTP_404_NOT_FOUND)


class ColumnAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsBoardOwner]

    @swagger_auto_schema(operation_summary="column list method")
    def get(self, requset, pk):
        board = Board.objects.get(pk=pk)
        column = board.column.all()
        serializer = ColumnSerializer(column, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ColumnSerializer, operation_summary="column create method")
    def post(self, request, pk):
        data = request.data
        board = Board.objects.get(pk=pk)
        serializer = ColumnSerializer(board, data)
        if serializer.is_valid():
            column = Column.objects.create(
                title=request.data['title'],
                board=board
            )
            column.save()
            return Response('successful created', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ColumnDetailView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsBoardOwner)

    @swagger_auto_schema(operation_summary="column get method")
    def get(self, request, column_id):
        column = Column.objects.get(id=column_id)
        if column:
            serializer = ColumnSerializer(column)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('column does not exists', status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=ColumnSerializer, operation_summary="update method")
    def patch(self, request, column_id):
        column = Column.objects.get(id=column_id)
        serializer = ColumnSerializer(column, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="delete method")
    def delete(self, request, column_id):
        column = Column.objects.get(id=column_id)
        if column:
            column.delete()
            return Response('Board successfully deleted', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Board not found', status=status.HTTP_404_NOT_FOUND)


class CardAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsBoardOwner)

    @swagger_auto_schema(operation_summary="column list method")
    def get(self, requset, column_id):
        column = Column.objects.get(pk=column_id)
        cards = column.cards.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CardSerializer, operation_summary='Creates a new Board Object')
    def post(self, request, column_id):
        data = request.data
        column = Column.objects.get(pk=column_id)
        serializer = CardSerializer(data=data)
        if serializer.is_valid():
            card = Card(
                title=request.data['title'],
                description=request.data['description']
            )
            card.column = column
            card.save()
            return Response('card successful created', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDetailView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsBoardOwner)

    def get_object(self, card_id):
        return Card.objects.get(pk=card_id)

    @swagger_auto_schema(operation_summary="column get method")
    def get(self, request, card_id):
        card = self.get_object(card_id)
        if card:
            serializer = CardSerializer(card)
            return Response(serializer.data)
        else:
            return Response('column does not exists', status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=CardSerializer, operation_summary="update method")
    def patch(self, request, card_id):
        card = self.get_object(card_id)
        serializer = ColumnSerializer(card, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="delete method")
    def delete(self, request, card_id):
        card = self.get_object(card_id)
        if card:
            card.delete()
            return Response('card successfully deleted', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Board not found', status=status.HTTP_404_NOT_FOUND)


class MarkAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsBoardOwner)

    @swagger_auto_schema(operation_summary="column list method")
    def get(self, requset, card_id):
        card = Card.objects.get(pk=card_id)
        marks = card.mark.all()
        serializer = CardSerializer(marks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MarkSerializer, operation_summary='Creates a new Mark Object')
    def post(self, request, card_id):
        data = request.data
        card = Card.objects.get(pk=card_id)
        serializer = MarkSerializer(data=data)
        if serializer.is_valid():
            mark = Mark(
                title=request.data['title'],
                color=request.data['color']
            )
            mark.card = card
            mark.save()
            return Response('mark successful created', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarkDetailView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsBoardOwner)

    def get_object(self, mark_id):
        return Card.objects.get(pk=mark_id)

    @swagger_auto_schema(operation_summary="mark get method")
    def get(self, request, mark_id):
        mark = self.get_object(mark_id)
        if mark:
            serializer = MarkSerializer(mark)
            return Response(serializer.data)
        else:
            return Response('mark does not exists', status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=MarkSerializer, operation_summary="update method")
    def patch(self, request, mark_id):
        mark = self.get_object(mark_id)
        serializer = MarkSerializer(mark, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="delete method")
    def delete(self, request, mark_id):
        mark = self.get_object(mark_id)
        if mark:
            mark.delete()
            return Response('mark successfully deleted', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Mark not found', status=status.HTTP_404_NOT_FOUND)


class CommentAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsBoardOwner)

    @swagger_auto_schema(operation_summary="comment list method")
    def get(self, requset, card_id):
        card = Card.objects.get(pk=card_id)
        comment = card.comment.all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CommentSerializer, operation_summary='Creates a new Comment Object')
    def post(self, request, card_id):
        data = request.data
        card = Card.objects.get(pk=card_id)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            comment = Comment(
                text=request.data['text'],
            )
            comment.created_on = datetime.datetime.now()
            comment.author = request.user
            comment.card = card
            comment.save()
            return Response('comment successful created', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsBoardOwner)

    def get_object(self, comment_id):
        return Comment.objects.get(pk=comment_id)

    @swagger_auto_schema(operation_summary="comment get method")
    def get(self, request, comment_id):
        comment = self.get_object(comment_id)
        if comment:
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            return Response('mark does not exists', status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(operation_summary="delete method")
    def delete(self, request, comment_id):
        comment = self.get_object(comment_id)
        if comment:
            comment.delete()
            return Response('comment successfully deleted', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Mark not found', status=status.HTTP_404_NOT_FOUND)


class FileAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsBoardOwner)

    @swagger_auto_schema(operation_summary="file list method")
    def get(self, requset, card_id):
        card = Card.objects.get(pk=card_id)
        files = card.files.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=FileSerializer, operation_summary='Creates a new Comment Object')
    def post(self, request, card_id):
        data = request.data
        card = Card.objects.get(pk=card_id)
        serializer = FileSerializer(data=data)
        if serializer.is_valid():
            file = serializer.save()
            file.card = card
            file.save()
            return Response('comment successful created', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDetailView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsBoardOwner)

    def get_object(self, file_id):
        return Comment.objects.get(pk=file_id)

    @swagger_auto_schema(operation_summary="file get method")
    def get(self, request, file_id):
        file = self.get_object(file_id)
        if file:
            serializer = CommentSerializer(file)
            return Response(serializer.data)
        else:
            return Response('mark does not exists', status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(operation_summary="file delete method")
    def delete(self, request, file_id):
        file = self.get_object(file_id)
        if file:
            file.delete()
            return Response('comment successfully deleted', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Mark not found', status=status.HTTP_404_NOT_FOUND)


class ChecklistAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsBoardOwner)

    @swagger_auto_schema(operation_summary="Checklist list method")
    def get(self, requset, card_id):
        card = Card.objects.get(pk=card_id)
        check_list = card.check_list.all()
        serializer = CommentSerializer(check_list, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ChecklistSerializer, operation_summary='Creates a new Checklist Object')
    def post(self, request, card_id):
        data = request.data
        card = Card.objects.get(pk=card_id)
        serializer = ChecklistSerializer(data=data)
        if serializer.is_valid():
            check_list = Checklist(
                title=request.data['title'],
            )
            check_list.card = card
            check_list.save()
            return Response('Checklist successful created', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChecklistDetailView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsBoardOwner)

    def get_object(self, check_id):
        return Comment.objects.get(pk=check_id)

    @swagger_auto_schema(operation_summary="check_list get method")
    def get(self, request, check_id):
        check_list = self.get_object(check_id)
        if check_list:
            serializer = ChecklistSerializer(check_list)
            return Response(serializer.data)
        else:
            return Response('Checklist does not exists', status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=ChecklistSerializer, operation_summary="update method")
    def patch(self, request, mark_id):
        check_list = self.get_object(mark_id)
        serializer = ChecklistSerializer(check_list, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="file delete method")
    def delete(self, request, check_id):
        check_list = self.get_object(check_id)
        if check_list:
            check_list.delete()
            return Response('Checklist successfully deleted', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Checklist not found', status=status.HTTP_404_NOT_FOUND)


class Archive(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsBoardOwner)

    @swagger_auto_schema(operation_description='archive board list')
    def get(self, request):
        queryset = Board.objects.filter(is_active=False)
        serializer = BoardSerializer(queryset, many=True)
        return Response(serializer.data)


class FavoriteView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsBoardOwner)

    def post(self, request, board_pk):
        board = Board.objects.filter(pk=board_pk)
        if board:
            object = Favorite(
                owner=request.user,
                board=board[0],
            )
            object.save()
            return Response('successful added', status=status.HTTP_201_CREATED)
        return Response('object does not exists', status=status.HTTP_400_BAD_REQUEST)


class FavoriteListView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema()
    def get(self, request):
        queryset = Favorite.objects.all()
        serializer = FavoriteSerializer(queryset, many=True)
        return Response(serializer.data)


class MemberView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )

    def post(self, request, board_pk):
        # board = Board.objects.get(pk=board_pk)
        board = get_object_or_404(Board, pk=board_pk)
        if board:
            object = Member(
                user=request.user,
                board=board,
            )
            object.save()
            return Response('successful added', status=status.HTTP_201_CREATED)
        return Response('object does not exists', status=status.HTTP_400_BAD_REQUEST)


class MemberListView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        queryset = Member.objects.all()
        serializer = MemberSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
