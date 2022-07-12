from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from .forms import SearchForm,EmailPostForm,CommentForm,StoryForm
from django.core.mail import send_mail
from .models import Post,Comment
import requests
from taggit.models import Tag
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
import http.client,urllib.parse

conn = http.client.HTTPConnection('api.mediastack.com')
params = urllib.parse.urlencode({
    'access_key': 'ACCESS_KEY',
    'categories': '-general,-sports,-politics',
    'sort': 'published_desc',
    'limit': 10,
    })

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(CACHE_TTL)
def home(request):
    response = requests.get('https://jsonplaceholder.typicode.com/todos/')
    news = response.json()
    return render(request,'Blog/base.html')

@cache_page(CACHE_TTL)
def post_list(request,tag_slug=None):
    posts_all = Post.published.all()
    
    paginator = Paginator(posts_all, 6)
    page = request.GET.get('page')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        posts_all = posts_all.filter(tags__in=[tag]) 
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post = paginator.page(paginator.num_pages)

    return render(request, 'Blog/post/post_list.html', {'page': page,'tag':tag, 
                                                        'post': post})


@cache_page(CACHE_TTL)
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    New_comments = None
    if request.method=='POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            New_comments = comment_form.save(commit=False)
            New_comments.post = post
            New_comments.save()
    else:
        comment_form = CommentForm()

    return render(request,
                  'Blog/post/detail.html',
                  {'post': post, 'comments': comments, 'New_comments': New_comments,
                   'comment_form': comment_form})

def share_post(request,post_id):
    post = get_object_or_404(Post,id= post_id, status='published')
    sent = False
    if request.method=='POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}  recommends  you read {post.title}"
            message = f"Read{post.title} at {post_url}{cd['name']}"
            send_mail(subject, message, 'titusnjuguna59@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'Blog/post/share_post.html',{'form':form,
    'post':post,'sent':sent})    

def Search_post(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)
            return render(request,
                          'Blog/base.html',
                          {'form': form,
                              'query': query,
                              'results': results})


def contact(request):
    return render(request,'Blog/contact-us.html') 

def shareContent(request):
    if request.method == 'POST':
        form = StoryForm()
    return render(request,'Blog/Share_story.html',{'form':form})
