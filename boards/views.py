import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, FormView, DetailView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.views.generic.edit import BaseUpdateView

from .forms import BoardCreationForm
from .models import Board, Card, Column


class FavoriteView(TemplateView):
    template_name = 'favorite.html'


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
        form = BoardCreationForm(request.POST, request.FILES)
        if form.is_valid():
            board = Board.objects.create(
                title=form.cleaned_data["title"],
                background=form.cleaned_data["background"],
                owner=request.user
            )
            board.save()
            print(request, request.POST)
        return HttpResponseRedirect(reverse_lazy('board_index'))


class BoardUpdateView(UpdateView):
    model = Board
    fields = ['title', 'background']
    template_name = 'update_form.html'

    def get_success_url(self):
        return '/'


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


class CardDetailView(DetailView):
    model = Card
    template_name = 'card_detail.html'

    def get_context_data(self, **kwargs ):
        context = super().get_context_data(**kwargs)
        context['current_card'] = Card.objects.get(id=kwargs['card_id']),
        context['columns'] = Column.objects.all()
        return context


def view_card(request, card_id):
    return render(request, template_name='card_detail.html', context={
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


class BoardDeleteView(DeleteView):
    model = Board
    success_url = '/'
    template_name = 'board_delete.html'


class ColumnDeleteView(DeleteView):
    model = Column
    template_name = 'column_confirm_delete.html'

    def get_success_url(self):
        print(self.kwargs.values())
        return reverse_lazy('board_index')


class ColumnUpdateView(UpdateView):
    model = Column
    fields = ["title"]
    template_name = 'column_update.html'

    def get_success_url(self):
        return reverse_lazy('board_index')


def delete_card(request, card_id):
    object_to_delete = get_object_or_404(Card, pk=card_id).delete()
    return redirect('/')


def update_card(request, card_id):
    card = Card.objects.get(id=card_id)
    template_name = 'card_update.html'
    context = {
        'card': card,
    }
    return render(request, template_name, context)

