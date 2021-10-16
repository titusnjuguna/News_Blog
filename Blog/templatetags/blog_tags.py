from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
register = template.Library()


@register.simple_tag
def total_post():
    return Post.published.count()


@register.inclusion_tag('Blog/post/latest_posts.html')
def show_latest_post(count=5):
    latest_post = Post.published.order_by('-publish')[:count]
    return {'latest_post': latest_post}


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


# @register.simple_tag
# def get_most_commented_posts(count=5):
#    return Post.published.annotate(
#        total_comments=Count('comments')
 #   ).order_by('-total_comments')[:count]
