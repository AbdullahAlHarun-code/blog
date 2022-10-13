from django.contrib import admin
from .models import Post
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