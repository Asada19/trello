import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, FormView, DetailView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormMixin

from .forms import BoardCreationForm, CommentForm, CardForm
from .models import Board, Card, Column, Comment


class FavoriteView(TemplateView):
    template_name = 'favorite.html'


class BoardListView(ListView):
    model = Board
    template_name = 'board/board_index.html'
    context_object_name = 'boards'


class BoardDetailView(DetailView):
    model = Board
    template_name = 'board/board_detail.html'


class BoardCreateView(CreateView):
    model = Board
    form_class = BoardCreationForm
    template_name = 'board/board_create.html'

    def post(self, request):
        form = BoardCreationForm(request.POST, request.FILES)
        if form.is_valid():
            board = Board.objects.create(
                title=form.cleaned_data["title"],
                background=form.cleaned_data["background"],
                owner=request.user
            )
            board.save()
        return HttpResponseRedirect(reverse_lazy('board_index'))


class BoardUpdateView(UpdateView):
    model = Board
    fields = ['title', 'background']
    template_name = 'board/update_form.html'

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


class CardDetailView(DetailView, LoginRequiredMixin, FormMixin):
    model = Card
    template_name = 'boards/card_detail.html'
    context_object_name = 'card'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        card = self.get_object()
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(card=card)
        context['form'] = self.get_form()
        return context

    def post(self, request, **kwargs):
        card = get_object_or_404(Card, id=kwargs['card_id'])
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = Comment(
                author=request.user,
                text=form.cleaned_data["text"],
                card=card
            )
            comment.save()
        comments = Comment.objects.filter(card=card)
        context = {
            "card": card,
            "card_title": card.title,
            "card_description": card.description,
            "comments": comments,
            "form": form
        }
        return render(request, "card/card_detail.html", context)


def view_card(request, card_id):
    return render(request, template_name='card/card_detail.html', context={
        'columns': Column.objects.all(),
        'card': Card.objects.get(id=card_id),
    })


class BoardDeleteView(DeleteView):
    model = Board
    success_url = '/'
    template_name = 'board/board_delete.html'


class ColumnDeleteView(DeleteView):
    model = Column
    template_name = 'board/column_confirm_delete.html'

    def get_success_url(self):
        print(self.kwargs.values())
        return reverse_lazy('board_index')


class ColumnUpdateView(View):
    def get(self, request, **kwargs):
        board = Board.objects.get(pk=kwargs['pk'])
        column = Column.objects.get(pk=kwargs['column_id'])
        template = get_template('board/column_update.html')
        context = {
            "board": board,
            "column": column
        }
        return HttpResponse(template.render(context, request))

    def post(self, request, **kwargs):
        board = Board.objects.get(pk=kwargs['pk'])
        column = Column.objects.get(pk=kwargs['column_id'])
        column.title = request.POST['title']
        column.save()
        return HttpResponseRedirect(reverse('board_detail', args=(board.id, )))

    def delete(self, **kwargs):
        board = Board.objects.get(pk=kwargs['pk'])
        column = Column.objects.get(pk=kwargs['column_id'])
        column.delete()
        return HttpResponseRedirect(reverse('board_detail', args=(board.id, )))


class CardUpdateView(View):

    def get(self, request, **kwargs):
        card = Card.objects.get(pk=kwargs['card_id'])
        board = card.column.board
        template = get_template('card/card_update.html')
        context = {
            'board': board,
            'card': card
        }
        return HttpResponse(template.render(context, request))

    def post(self, request, **kwargs):
        card = Card.objects.get(pk=kwargs['card_id'])
        board = card.column.board
        form = CardForm(request.POST)
        card.title = request.POST['title']
        # card.date_of_end = request.POST['date_of_end']
        card.description = request.POST['description']
        # # card.members = request.POST['member']
        # # card.file = request.POST.get('file')
        # card.comment = request.POST['comment']
        # # card.mark = request.POST('mark')
        # # card.check_list = request.POST.get('check_list')
        card.save()
        return HttpResponseRedirect(reverse('card_detail', args=(card.pk, )))

    def delete(self, **kwargs):
        card = Card.objects.get(pk=kwargs['card_id'])
        board = card.column.board
        card.delete()
        return HttpResponseRedirect(reverse('board_detail', args=(board.pk, )))

    def drop(request):
        payload = json.loads(request.body)
        card_id = int(payload.get('card_id'))
        column_id = int(payload.get('column_id'))
        assert card_id and column_id
        card = Card.objects.get(id=card_id)
        card.column = Column.objects.get(id=column_id)
        card.save()
        return HttpResponse()

