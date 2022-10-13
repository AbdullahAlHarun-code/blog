from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.
def post_list_view(request):
    posts = Post.objects.all()
    template_name = 'blog/post/post_list.html'
    context = {'posts':posts}
    return render(request, template_name, context)

def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    template_name = 'blog/post/post_detail.html'
    context = {'post':post}
    return render(request, template_name, context)
