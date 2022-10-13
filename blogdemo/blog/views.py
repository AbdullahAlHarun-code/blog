from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm

# Create your views here.
class PostListView(ListView):
    queryset = Post.objects.all().filter(status=Post.Status.PUBLISHED)
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/post_list.html'

def post_list_view(request):
    posts = Post.objects.all().filter(status=Post.Status.PUBLISHED)
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


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    template_name = 'blog/post/share.html'
    context = {'post':post, 'form': form}
    return render(request, template_name, context)