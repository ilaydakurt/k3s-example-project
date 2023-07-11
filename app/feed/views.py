from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework import mixins
from rest_framework.generics import UpdateAPIView, DestroyAPIView


from .serializers import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.models import User
from app.settings import DOMAIN_URL
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_filters.rest_framework import DjangoFilterBackend
import uuid
import re
import random

import requests
from django.http import JsonResponse

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()
    paginate_by = 2

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        print(request.data)
        post_link = request.data.get("post_link")
        existing_post = Post.objects.filter(post_link=post_link).first()
        is_confirmed = request.data.get("is_confirmed")
        user = User.objects.filter(id=request.user.id).first()
        request.data["owner"] = user.id
        if existing_post and not is_confirmed:
            data = Post.objects.all().order_by("-id")
            posts = PostListSerializer(data, many=True).data
            return render(
                request,
                "posts.html",
                {
                    "posts": posts,
                    "owner": user.first_name + " " + user.last_name,
                    "DOMAIN_URL": DOMAIN_URL,
                    "title": request.data.get("title"),
                    "description": request.data.get("description"),
                    "platform": request.data.get("platform"),
                    "post_link": request.data.get("post_link"),
                    "confirmation_modal": True
                },
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = Post.objects.all().order_by("-id")
        posts = PostListSerializer(data, many=True).data
        headers = self.get_success_headers(serializer.data)
        created_post_obj = Post.objects.get(id=serializer.data["id"])
        return render(
            request,
            "posts.html",
            {
                "posts": posts,
                "owner": user.first_name + " " + user.last_name,
                "DOMAIN_URL": DOMAIN_URL,
            },
        )


    @action(detail=False, methods=["get"], name="Liked Posts")
    def own_posts(self, request, pk=None):
        user = User.objects.filter(id=request.user.id).first()
        data = Post.objects.filter(owner=user.id).order_by("-id")
        posts = PostListSerializer(data, many=True).data

        # return Response({"detail":"Liked succesfully"},status=200)
        return render(
            request,
            "yourPosts.html",
            {
                "posts": posts,
                "owner": user.first_name + " " + user.last_name,
                "DOMAIN_URL": DOMAIN_URL,
            },
        )

    def list(self, request, *args, **kwargs):
        data = Post.objects.all().order_by("-id")
        posts = PostListSerializer(data, many=True).data
        print('is_confirmed:', request.data.get("is_confirmed"))
        if request.user.is_anonymous == False:
            user = request.user
            return render(
                request,
                "posts.html",
                {
                    "posts": posts,
                    "owner": user.first_name + " " + user.last_name,
                    "DOMAIN_URL": DOMAIN_URL,
                },
            )
        else:
            # return Response(PostListSerializer(posts,many=True).data,status=200)
            return render(
                request, "posts.html", {"posts": posts, "DOMAIN_URL": DOMAIN_URL}
            )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Deleted successfully", status=200)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "retrieve" or self.action == "list":
            return PostListSerializer
        else:
            return PostCreateSerializer

    def get_permissions(self):
        if self.action == "retrive" or self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
