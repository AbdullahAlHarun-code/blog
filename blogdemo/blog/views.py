from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_list_view(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3) # 3 post per page
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except:
        posts = paginator.page(paginator.num_pages)
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
