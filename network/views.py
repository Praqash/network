from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import*
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm 
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError


def index(request):
    user = User.objects.filter(username=request.user.username).first()
    if hasattr(user, 'profile'):
        context={'posts': Post.objects.all().order_by('-timestamp'), 'profile_picture' : user.profile.profile_picture}
    else:
        context={'posts': Post.objects.all().order_by('-timestamp')}
    return render(request, "network/index.html", context)

def layout(request):
    context={'posts': Post.objects.all().order_by('-timestamp')}
    return render(request, "network/layout", context)


def profile(request, **kwargs):
    l2=[]
    l3=[]
    id = kwargs.get('username')
    k= Post.objects.filter(username__username=id).order_by("-timestamp")
    l= get_object_or_404(User, username=id)
    length= (l.followed.all().values('id'))
    post= Post.objects.all().filter(username=request.user)
    user = User.objects.filter(username=request.user.username).first()
    for i in (post):
        l3.append([i.like_count, i.id])
    for i in range(len(length)):
        l2.append((length[i]['id']))
    displaybool = str(request.user) != str(id)
    followbool = str(l.followed.all) != None
    if hasattr(user, 'profile'):
        context={'k' : k, 'l':l ,'displaybool':displaybool, 'followbool':followbool, 'l2':l2, 'l3':l3, 'posts': Post.objects.all().order_by('-timestamp'), 'profile_picture' : user.profile.profile_picture}
    else:
        context= {'k' : k, 'l':l ,'displaybool':displaybool, 'followbool':followbool, 'l2':l2, 'l3':l3 }
    return render(request, "network/profile.html", context )


def follow(request):
    user_id = request.GET.get('id', None)

    if not user_id:
        return JsonResponse({'error': 'User ID not provided'})

    try:
        user_id = int(user_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid User ID'})

    user_to_follow = get_object_or_404(User, id=user_id)

    try:
        if user_to_follow.followed.filter(id=request.user.id).exists():
            user_to_follow.followed.remove(request.user)
            user_to_follow.save()
            return JsonResponse({'val': "Follow Me"})
        else:
            user_to_follow.followed.add(request.user)
            user_to_follow.save()
            return JsonResponse({'val': "Followed"})
    except IntegrityError as e:
        return JsonResponse({'error': str(e)})
     

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
        d.save()
        return JsonResponse({"data":new_post})
        



def like(request):
    if request.method == 'GET':
        pid = request.GET['post_i']
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
        username = username.capitalize()
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



@login_required
def edit_profile(request):
    try:
        # Try to get the current user's profile
        profile = Profile.objects.get(username=request.user)
    except Profile.DoesNotExist:
        # If the profile doesn't exist, create a new one
        profile = Profile(username=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Error updating profile. Please correct the errors.')
    else:
        # Set the username field value before rendering the form
        form = ProfileForm(instance=profile, initial={'username': request.user.username})

    return render(request, "network/edit_profile.html", {'form': form})

def show_profile_picture(request):
    user = User.objects.filter(username=request.user.username).first()
    print(user.profile.profile_picture)
    context={'profile_picture' : user.profile.profile_picture}
    return render(request, "network/show_profile_picture.html", context)