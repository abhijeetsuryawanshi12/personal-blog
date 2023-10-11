from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Post, Comment
from django.views import View
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from .forms import CommentForm

from django.views.generic import ListView, DetailView

all_posts = [
    {
        "slug": "AI future",
        "image": "AI.jpg",
        "author": "Abhijeet",
        "date": date(2023,10,7),
        "title": "AI World",
        "excerpt": "There is nothing like the views where you can hike in the Mountains! And I wasn't even prepared",
        "content": """
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. 
            Obcaecati temporibus sit recusandae ex doloribus, 
            laborum illo maiores quo iste explicabo dolorum facere ut. 
            Labore officia consequuntur qui tempore voluptate saepe!
            
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. 
            Obcaecati temporibus sit recusandae ex doloribus, 
            laborum illo maiores quo iste explicabo dolorum facere ut. 
            Labore officia consequuntur qui tempore voluptate saepe!
            
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. 
            Obcaecati temporibus sit recusandae ex doloribus, 
            laborum illo maiores quo iste explicabo dolorum facere ut. 
            Labore officia consequuntur qui tempore voluptate saepe!"""
    },

    {
        "slug": "Nature is Piece",
        "image": "nature.avif",
        "author": "Abhijeet",
        "date": date(2023,12,7),
        "title": "Mountain Hiking",
        "excerpt": "There is nothing like the views where you can hike in the Mountains! And I wasn't even prepared",
        "content": """
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. 
            Obcaecati temporibus sit recusandae ex doloribus, 
            laborum illo maiores quo iste explicabo dolorum facere ut. 
            Labore officia consequuntur qui tempore voluptate saepe!
            
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. 
            Obcaecati temporibus sit recusandae ex doloribus, 
            laborum illo maiores quo iste explicabo dolorum facere ut. 
            Labore officia consequuntur qui tempore voluptate saepe!
            
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. 
            Obcaecati temporibus sit recusandae ex doloribus, 
            laborum illo maiores quo iste explicabo dolorum facere ut. 
            Labore officia consequuntur qui tempore voluptate saepe!"""
    },

    {
        "slug": "Mountain Hiking",
        "image": "mountain.avif",
        "author": "Abhijeet",
        "date": date(2023,11,7),
        "title": "Nature is love",
        "excerpt": "There is nothing like the views where you can hike in the Mountains! And I wasn't even prepared",
        "content": """
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. 
            Obcaecati temporibus sit recusandae ex doloribus, 
            laborum illo maiores quo iste explicabo dolorum facere ut. 
            Labore officia consequuntur qui tempore voluptate saepe!
            
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. 
            Obcaecati temporibus sit recusandae ex doloribus, 
            laborum illo maiores quo iste explicabo dolorum facere ut. 
            Labore officia consequuntur qui tempore voluptate saepe!
            
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. 
            Obcaecati temporibus sit recusandae ex doloribus, 
            laborum illo maiores quo iste explicabo dolorum facere ut. 
            Labore officia consequuntur qui tempore voluptate saepe!"""
    }
]



# Create your views here.

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {
#         "posts": latest_posts
#     })

class AllPostView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html", { 
#         "all_posts":all_posts})

class SinglePostView(View):
    # template_name = "blog/post-detail.html"
    # model = Post
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later
    
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        else:
             print(comment_form.errors)
        context = {
                "post": post,
                "post_tags": post.tags.all(),
                "comment_form": CommentForm(),
                "comments": post.comments.all().order_by("-id"),
                "saved_for_later": self.is_stored_post(request, post.id)
            }
        
        return render(request, "blog/post-detail.html", context)

class ReadLaterView(View):
     
     def get(self, request):
        stored_posts = request.session.get("stored_posts")
        
        context = {}

        if stored_posts is None or len(stored_posts)==0:
            context["post"] = []
            context["has_power"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        
        return render(request, "blog/stored-posts.html", context)

     def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id )
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")

    # def get_context_data(self, **kwargs: Any):
    #     context = super().get_context_data(**kwargs)
    #     context["post_tags"] = self.object.tags.all()
    #     context["comment_form"] = CommentForm()
    #     return context

# def post_detail(request,slug):
#     identified_post = get_object_or_404(Post,slug=slug)
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post,
#         "post_tags": identified_post.tags.all()
#     } )