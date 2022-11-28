from django.http import Http404, JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BoardSerializer, BoardDetailSerializer, ColumnSerializer
from ..models import Board, Column


class BoardAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(operation_summary='List all Board Objects')
    def get(self, request):
        boards = Board.objects.filter(owner=[request.user.id][0])
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

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
        if serializer:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    @swagger_auto_schema(operation_summary="column get method")
    def get(self, request, column_id):
        column = Column.objects.get(id=column_id)
        serializer = ColumnSerializer(column)
        return Response(serializer.data)


