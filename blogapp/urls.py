from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('post_list/', views.post_list, name='post_list'),
    path('contact/', views.contact, name='contact'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    path('tag/<slug:tag_slug>/',
         views.post_list, name='post_list_by_tag'),
    path('<int:post_id>/comment/',
         views.post_comment, name='post_comment'),
    # reply to comment
    path('<int:post_id>/comment/<int:comment_id>/', views.post_comment, name='reply_comment'),
    path('search/', views.post_search, name='post_search'),
    # search results
    path('search/', views.post_search, name='search'),
    # like post
    path('<int:post_id>/like/', views.post_like, name='post_like'),
]
