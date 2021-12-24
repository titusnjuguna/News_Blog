from django.urls import path
from .feeds import LatestPostsFeed
from . import views
from .templatetags import blog_tags
app_name = 'Blog'

urlpatterns = [
    
    path('', views.post_list, name='Post_List'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail,name='post_detail'),
    path('<int:post_id>/share/', views.share_post, name='share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.Search_post, name='post_search'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('contact/', views.contact, name='contact'),
    path('Share_story/', views.shareContent, name='content'),
]
