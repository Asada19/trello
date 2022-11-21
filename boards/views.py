import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, FormView, DetailView

from .forms import BoardCreationForm
from .models import Board, Card, Column


class BoardListView(ListView):
    model = Board
    template_name = 'board_index.html'
    context_object_name = 'boards'


class BoardDetailView(DetailView):
    model = Board
    template_name = 'board_detail.html'


class BoardCreateView(CreateView):
    model = Board
    form_class = BoardCreationForm
    template_name = 'board_create.html'

    def post(self, request):
        form = BoardCreationForm(request.POST)
        if form.is_valid():
            board = Board.objects.create(
                title=form.cleaned_data["title"],
                background=form.cleaned_data["background"],
                owner=request.user
            )
            board.save()
        return HttpResponseRedirect(reverse_lazy('board_index'))


def new_card(request):
    column_id = request.POST.get('column_id')
    title = request.POST.get('title')
    assert title and column_id
    Card.objects.create(title=title, column_id=column_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def new_column(request, pk):
    board_id = Board.objects.get(id=pk)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    title = body['title']
    assert title and board_id
    Column.objects.create(title=title, board_id=board_id.id)
    return redirect('board_detail', pk)


def view_card(request, card_id):
    return render(request, template_name='view.html', context={
        'columns': Column.objects.all(),
        'current_card': Card.objects.get(id=card_id),
    })


def drop(request):
    payload = json.loads(request.body)
    card_id = int(payload.get('card_id'))
    column_id = int(payload.get('column_id'))
    assert card_id and column_id
    card = Card.objects.get(id=card_id)
    card.column = Column.objects.get(id=column_id)
    card.save()
    return HttpResponse()
