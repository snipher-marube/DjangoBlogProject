from django.contrib.auth.models import User
from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib import messages

from .models import Post, Video
from .forms import EmailPostForm, CommentForm, SearchForm, ContactForm

def home(request):
    posts = Post.published.all().order_by('publish')
    # get all tags
    tags = Tag.objects.all()[:4]
    more_tags = Tag.objects.all()[4:100]
    side_posts = Post.published.all().order_by('-publish')[:7]
    featured_posts = Post.published.all().filter(featured=True).order_by('-featured')[:2]

    posts_slides = Post.published.all()[0:4]
    posts_slides2 = Post.published.all()[4:8]
    home_featured = Post.published.all().filter(featured=True).order_by('-featured')[:3]
    # get top stories
    top_stories = Post.published.all().order_by('publish')[:5]

    # today picks
    today_picks = Post.published.all().order_by('featured')[:1]
    context = {
        'posts': posts,
        'tags': tags,
        'more_tags': more_tags,
        'side_posts': side_posts,
        'featured_posts': featured_posts,
        'posts_slides': posts_slides,
        'posts_slides2': posts_slides2,
        'home_featured': home_featured,
        'top_stories': top_stories,
        'today_picks': today_picks,
    }
    return render(request, 'blog/home.html', context)


def post_list(request, tag_slug=None):
    posts = Post.published.all()

    posts_slides = Post.published.all()[0:4]
    posts_slides2 = Post.published.all()[4:8]
    videos = Video.objects.all()[0:2]

    # get top stories
    top_stories = Post.published.all().order_by('publish')[:5]

    # today picks
    today_picks = Post.published.all().order_by('-publish')[:1]

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 4)  # 4 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)


    # get all tags
    tags = Tag.objects.all()[:4]
    more_tags = Tag.objects.all()[4:100]
    # assign tags to posts
    if posts:
        for post in posts:
            post.tags = post.tags.all()

    # featured posts
    featured_posts = Post.published.all().filter(featured=True)[:3]

    context = {
        'posts': posts,
        'tag': tag,
        'posts_slides': posts_slides,
        'videos': videos,
        'top_stories': top_stories,
        'posts_slides2': posts_slides2,
        'today_picks': today_picks,
        'tags': tags,
        'more_tags': more_tags,
        'featured_posts': featured_posts,

    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # form for new comment
    form = CommentForm()
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]

    # get top stories
    top_stories = Post.published.all().order_by('publish')[:5]

    # today picks
    today_picks = Post.published.all().order_by('-publish')[:1]

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,
        'top_stories': top_stories,
        'today_picks': today_picks,
    }

    return render(request, 'blog/post_detail.html', context)

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            sent = True
    else:
        form = EmailPostForm()
    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }
    return render(request, 'blog/share.html', context)

def post_search(request):
    # get search query
    query = request.GET.get('query')
    results = []
    if query:
        # search in title and body
        results = Post.objects.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')
    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'blog/search.html', context)


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            form = ContactForm()

    context = {
        'form': form,
    }

    return render(request, 'blog/contact.html', context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the current post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return redirect('blog:post_detail', post.publish.year, post.publish.month, post.publish.day, post.slug)

# post like
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')

    # check if user is anonymous
    if request.user.is_anonymous:
        # get user ip
        ip = get_client_ip(request)
        # convert ip to int
        ip = int(ip.replace('.', ''))
        # make sure ip is not in the list
        if ip not in post.likes.all():
            post.likes.add(ip)
            post.save()
            return redirect('blog:post_detail', post.publish.year, post.publish.month, post.publish.day, post.slug)



    else:
        # check if user has liked post
        if post.likes.filter(id=request.user.id).exists():
            # user has already liked post
            post.likes.remove(request.user)
            messages.success(request, 'You disliked this post')
        else:
            # user has not liked post
            post.likes.add(request.user)
            messages.success(request, 'You liked this post')

    return redirect('blog:post_detail', post.publish.year, post.publish.month, post.publish.day, post.slug)