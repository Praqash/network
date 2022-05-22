from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import*
import json

def index(request):
    context={'posts': Post.objects.all().order_by('-timestamp')}
    return render(request, "network/index.html", context)

def layout(request):
    context={'posts': Post.objects.all().order_by('-timestamp')}
    return render(request, "network/layout", context)


def profile(request, **kwargs):
    l2=[]
    id = kwargs.get('username')
    k= Post.objects.filter(username__username=id)
    l= get_object_or_404(User, username=id)
    length= (l.followed.all().values('id'))
    for i in range(len(length)):
        l2.append((length[i]['id']))
   

    displaybool = str(request.user) != str(id)
    followbool = str(l.followed.all) != None
    context= {'k' : k, 'l':l ,'displaybool':displaybool, 'followbool':followbool, 'l2':l2}
    return render(request, "network/profile.html", context )

def follow(request):
    id = request.GET['id']
    print(id)
    post= get_object_or_404(User, id=id)
    print(post)
    if post.followed.filter(id=request.user.id).exists():
        post.followed.remove(request.user.id)
        post.save()
        return JsonResponse({'val':"Follow Me"})
        
    else:
        
        post.followed.add(request.user.id)
        post.save()
        return JsonResponse({'val':"Followed"})
    
        
          

def com(request):
    if request.method == "POST":
        comment= request.POST["comment"]    
        c = Post(content=comment, username= request.user)
        c.save()
        return HttpResponseRedirect(reverse("index"))

def trash(request):
    if request.method == 'GET':
        user=(request.user)
        print(user.id)
        pid = request.GET['post_d']
        d = Post.objects.get(id = pid )
        print(d)
        d.delete()
        return JsonResponse({"data":pid})
           
def update(request):
    if request.method == "POST":
        new_post= request.POST["po"]    
        id = request.POST['n']
        d = Post.objects.get(id = id)
        d.content= new_post
        print(d.content)
        d.save()
        return JsonResponse({"data":new_post})
        



def like(request):
    if request.method == 'GET':
        user=(request.user)
        print(user.id)
        pid = request.GET['post_i']
        d = Post.objects.get(id = pid )
        print(d)
        post= get_object_or_404(Post, id=pid)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result= post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count +=1
            result = post.like_count
            post.save()
            
        if post.likes.filter(id=request.user.id).exists():

            return JsonResponse({'result':result, 'val':"red"
            })
        else:
            return JsonResponse({'result':result, 'val':"#D3D3D3"})
    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
