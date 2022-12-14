from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from slugify import slugify
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag 
from django.db.models import Count

# Create your views here.
class PostListView(ListView):
    queryset = Post.objects.all().filter(status=Post.Status.PUBLISHED)
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog/post/post_list.html'

def post_list_view(request, tag_slug=None):
    posts = Post.objects.all().filter(status=Post.Status.PUBLISHED)
    page_number = request.GET.get('page', 1)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 10) # 3 post per page
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except:
        posts = paginator.page(paginator.num_pages)
    template_name = 'blog/post/post_list.html'
    context = {'posts':posts, 'tag':tag}

    return render(request, template_name, context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,\
            slug=post,
            publish__year=year,
            publish__month=month,
            publish__day=day
        )
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:2]
    comments = post.comments.filter(active=True)
    form = CommentForm()
    template_name = 'blog/post/post_detail.html'
    context = {'post':post,'comments':comments, 'form': form, 'similar_posts':similar_posts}
    return render(request, template_name, context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    template_name = 'blog/post/share.html'
    context = {'post':post, 'form': form, 'sent':sent}
    return render(request, template_name, context)

def fakerdemo(request):
    from faker import Faker
    fk = Faker()
    for i in range(100):
        title=fk.sentence()
        ob_post = Post.objects.create(
            title=title,
            body = fk.paragraph(nb_sentences=180),
            author_id = 1,
            status=Post.Status.PUBLISHED,
            slug= slugify(title)
        )
    context = {
        'all_new_post': ob_post
    }
    return render(request, 'blog/facker.html',context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post 
        comment.save()
    template = 'blog/post/comment.html'
    context={
        'post':post,
        'form': form,
        'comment': comment
    }
    return render(request, template, context)
