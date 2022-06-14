import json

from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from django.shortcuts import get_object_or_404

from .models import Post, Like, Comment
from .settings import ITEM_LIMIT


class PostListView(View):
    """
    POST: Creates a Post.
    GET: List all the posts.
    """

    @method_decorator(login_required, name='get')
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, ITEM_LIMIT)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # if the given value is not number, then show the first page
            page = 1
            posts = paginator.page(page)
        except EmptyPage:
            # If a non existing page number is given show last page
            page = paginator.num_pages
            posts = paginator.page(page)

        data = []
        for post in posts:
            no_likes = Like.objects.filter(post=post).count()
            no_comments = Comment.objects.filter(post=post).count()
            data.append({
                'id': post.id,
                'title': post.title,
                'user_id': post.user.id,
                'user': str(post.user),
                'content': post.content,
                'no_likes': no_likes,
                'no_comments': no_comments,
                'pub_date': post.pub_time
            })
        return JsonResponse(data, status=200, safe=False)

    @method_decorator(login_required, name='post')
    def post(self, request, *args, **kwargs):
        if request.META['CONTENT_TYPE'] == "application/json":
            try:
                post_body = json.loads(request.body)
            except ValueError:
                return HttpResponseBadRequest("Incorrect Request format")
            try:
                title = post_body['title']
                content = post_body['content']
            except KeyError:
                return HttpResponseBadRequest("Missing Parameters")
            user = request.user
            post = Post.objects.create(
                title=title,
                content=content,
                user=user
            )
            return HttpResponse("Post Successfuly Created", status=201)
        else:
            return HttpResponseBadRequest("Unsupported content_type found.")


class PostDetailView(View):
    """
    DELETE: deletes a Post.
    GET: Gives Details about one post.
    """

    @method_decorator(login_required, name='get')
    def get(self, request, *args, **kwargs):
        post_id = kwargs.pop('post_id')
        try:
            post = get_object_or_404(Post, id=post_id)
        except ValueError:
            return HttpResponseBadRequest("Given id is not a number")
        likes_info = []
        likes = Like.objects.filter(post=post)
        for like in likes:
            likes_info.append({
                'id': like.id,
                'liked_user_id': like.user.id,
                'liked_user_name': str(like.user),
                'liked_time': like.liked_time
            })
        comments_info = []
        comments = Comment.objects.filter(post=post)
        for comment in comments:
            comments_info.append({
                'id': comment.id,
                'commented_user_id': comment.user.id,
                'commented_user_name': str(comment.user),
                'commented_time': comment.commented_time,
                'comment_description': comment.comment_description
            })

        data = {
            'id': post.id,
            'user_id': post.user.id,
            'user': post.user.profile_name,
            'title': post.title,
            'content': post.content,
            'likes': likes_info,
            'comments': comments_info,
            'pub_date': post.pub_time
        }
        return JsonResponse(data, status=200)

    @method_decorator(login_required, name='delete')
    def delete(self, request, *args, **kwargs):
        post_id = kwargs.pop('post_id')
        try:
            post = get_object_or_404(Post, id=post_id)
        except ValueError:
            return HttpResponseBadRequest("Given id is not a number")
        post.delete()
        return HttpResponse("Post Successfuly Deleted", status=200)


class CommentListView(View):
    """
    POST: Creates a Comment.
    """

    @method_decorator(login_required, name='post')
    def post(self, request, *args, **kwargs):
        if request.META['CONTENT_TYPE'] == "application/json":
            try:
                post_body = json.loads(request.body)
            except ValueError:
                return HttpResponseBadRequest("Incorrect Request format")
            try:
                post_id = post_body['post_id']
                description = post_body['description']
            except KeyError:
                return HttpResponseBadRequest("Missing Parameters")
            user = request.user
            try:
                comment = Comment.objects.create(
                    post_id=post_id,
                    comment_description=description,
                    user=user
                )
            except IntegrityError:
                return HttpResponseBadRequest("Invalid Post")
            return HttpResponse("Comment Successfuly Created", status=201)
        else:
            return HttpResponseBadRequest("Unsupported content_type found.")


class LikeListView(View):
    """
    POST: Creates a Like.
    """

    @method_decorator(login_required, name='post')
    def post(self, request, *args, **kwargs):
        if request.META['CONTENT_TYPE'] == "application/json":
            try:
                post_body = json.loads(request.body)
            except ValueError:
                return HttpResponseBadRequest("Incorrect Request format")
            try:
                post_id = post_body['post_id']
            except KeyError:
                return HttpResponseBadRequest("Missing Parameters")
            user = request.user
            try:
                like = Like.objects.create(
                    post_id=post_id,
                    user=user
                )
            except IntegrityError:
                return HttpResponseBadRequest(
                    "Already Liked This Post Or Invalid Post")
            return HttpResponse("Like Successfuly Created", status=201)
        else:
            return HttpResponseBadRequest("Unsupported content_type found.")
