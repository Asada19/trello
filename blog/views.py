from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import Post, Comment, Category
from .forms import CommentForm


class BlogListView(ListView):
    model = Post
    template_name = 'blog_index.html'
    ordering = '-created_on'
    context_object_name = 'posts'


class BlogCategoryView(ListView):
    model = Post
    ordering = ['-created_on', ]
    template_name = 'blog_category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(categories__name__contains=self.kwargs['category'])


class BlogDetailView(DetailView, FormView):
    model = Post
    form_class = CommentForm
    template_name = 'blog_detail.html'
    context = ['post', 'comments', 'form']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=kwargs['object']).order_by('-id')
        return context

    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post_id=pk
            )

        return HttpResponseRedirect(reverse_lazy('blog_detail', args=[pk]))

