from django.urls import path, re_path
from .views import PostListView, PostDetailView, CommentListView, LikeListView
urlpatterns = [
    re_path('post/?$', PostListView.as_view(), name='post_list'),
    re_path('post/(?P<post_id>\w{1,})/?$',
            PostDetailView.as_view(), name='post_detail'),
    re_path('like/?$', LikeListView.as_view(), name='like_list'),
    re_path('comment/?$', CommentListView.as_view(), name='comment_list'),

]
