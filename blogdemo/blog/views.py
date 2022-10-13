from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.
def post_list_view(request):
    posts = Post.objects.all()
    template_name = 'blog/post/post_list.html'
    context = {'posts':posts}
    return render(request, template_name, context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,\
            slug=post,
            publish__year=year,
            publish__month=month,
            publish__day=day
        )
    template_name = 'blog/post/post_detail.html'
    context = {'post':post}
    return render(request, template_name, context)
