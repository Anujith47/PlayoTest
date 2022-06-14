import json
import re

from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db import IntegrityError

from .models import SocialUser

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class HomeView(TemplateView):
    template_name = "home.html"


class LoginUserView(View):
    """
    GET: Serves the login page
    POST: Authenticates the user.
    """

    def get(self, request, *args, **kwargs):
        """
        created to just get the csrf token to postman."
        """
        return render(request, 'social_auth/login.html')

    def post(self, request, *args, **kwargs):
        if request.META['CONTENT_TYPE'] == "application/json":
            try:
                post_body = json.loads(request.body)
            except ValueError:
                return HttpResponseBadRequest("Incorrect request format")
            try:
                username = post_body['username']
                password = post_body['password']
            except KeyError:
                return HttpResponseBadRequest("Missing parameters")
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponse("Successfuly logged in", status=200)
            else:
                return HttpResponse("Invalid credentials", status=401)
        else:
            return HttpResponseBadRequest("Unsupported content_type found.")

class SocialUserListView(View):
    """
    POST: Creates a user.
    """
    def post(self, request, *args, **kwargs):
        if request.META['CONTENT_TYPE'] == "application/json":
            try:
                post_body = json.loads(request.body)
            except ValueError:
                return HttpResponseBadRequest("Incorrect request format")
            try:
                username = post_body['username']
                password = post_body['password']
                email = post_body['email']
                first_name = post_body['first_name']
                last_name = post_body['last_name']
                nick_name = post_body.get('nick_name', None)
            except KeyError:
                return HttpResponseBadRequest("Missing parameters")
            if len(password) < 8:
                return HttpResponseBadRequest(
                    "Password is not of adequate length")
            if not self._check_email(email):
                return HttpResponseBadRequest("Invalid email address")
            try:
                user = SocialUser.objects.create(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    nick_name=nick_name)
                login(request, user)
            except IntegrityError:
                return HttpResponseBadRequest("User name exists")
            return HttpResponse("Successfuly signed up", status=201)
        else:
            return HttpResponseBadRequest("Unsupported content_type found.")

    def _check_email(self, email):
        if(re.fullmatch(EMAIL_REGEX, email)):
            return True
        else:
            return False
