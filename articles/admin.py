from django.contrib import admin
from .models import Article, Comment

class CommentInline(admin.TabularInline):  # You can switch to StackedInline if preferred
    model = Comment
    extra = 1  # Number of empty forms to display

class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('title', 'author', 'date')  # Customize as needed
    search_fields = ('title', 'body')  # Optional: to make searching easier

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
