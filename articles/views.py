from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from .models import Article, Comment
from .forms import CommentForm

class ArticleListView(LoginRequiredMixin, ListView):  # Article list view
    model = Article
    template_name = "article_list.html"

class ArticleDetailView(LoginRequiredMixin, DetailView):  # Article detail view
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs):  # Include comment form in context
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()  # Include the comment form
        context['comments'] = self.object.comment_set.all()  # Include comments for the article
        return context

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # Article update view
    model = Article
    fields = ("title", "body")  # Specify fields to edit
    template_name = "article_edit.html"

    def test_func(self):  # Only allow the author to edit
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # Article delete view
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")  # Redirect after deletion

    def test_func(self):  # Only allow the author to delete
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleCreateView(LoginRequiredMixin, CreateView):  # Article creation view
    model = Article
    template_name = "article_new.html"
    fields = ("title", "body")

    def form_valid(self, form):  # Set the author to the current user
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin, FormView):  # Comment creation view
    form_class = CommentForm
    template_name = "article_detail.html"  # Use the article detail template for context

    def form_valid(self, form):  # Handle valid form submissions
        article = Article.objects.get(pk=self.kwargs['pk'])  # Get the article
        comment = form.save(commit=False)
        comment.article = article  # Associate the comment with the article
        comment.author = self.request.user  # Set the comment author
        comment.save()
        return redirect(article.get_absolute_url())  # Redirect to the article detail page

    def get_context_data(self, **kwargs):  # Pass additional context
        context = super().get_context_data(**kwargs)
        context['article'] = Article.objects.get(pk=self.kwargs['pk'])  # Pass the article to context
        context['form'] = self.get_form()  # Include the form in context
        context['comments'] = context['article'].comment_set.all()  # Include comments
        return context

    def get_success_url(self):  # Define the success URL after saving a comment
        article = Article.objects.get(pk=self.kwargs['pk'])
        return reverse("article_detail", kwargs={"pk": article.pk})
