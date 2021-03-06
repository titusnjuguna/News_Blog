from django import template
from ..models import Post,Comment
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.shortcuts import render, get_object_or_404
import markdown
import calendar
register = template.Library()


@register.simple_tag
def total_post():
    return Post.published.count()


@register.inclusion_tag('Blog/post/latest_posts.html')
def show_latest_post(count=5):
    latest_post = Post.published.order_by('-publish')[:count]
    return {'latest_post': latest_post}

@register.inclusion_tag('Blog/post/latest_posts_car.html')
def show_latest_post_carousel(count=5):
    latest_post_car = Post.published.order_by('-publish')[:count]
    return {'latest_post_car': latest_post_car}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter
def month_name(month_number):
    month_number = int(month_number)
    return calendar.month_name[month_number]

