from django.contrib import admin
from .models import Post, Comment
# Register your models here.
#admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status'] # list display in admin
    list_filter = ['status', 'created', 'publish', 'author'] # when we filter by this catetgory
    search_fields = ['title', 'body'] # search fields
    prepopulated_fields = {'slug': ('title',)} # when we create post and set title slug field aotomatic create by title
    date_hierarchy =  'publish' # 
    ordering = ['status', 'publish'] # 
    raw_id_fields = ['author'] # author field now select by user id

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_field = ['name', 'email', 'body']