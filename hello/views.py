from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from .models import Profile, Plant, Post, Comment
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError



def index(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user_id=request.user.id)
            requests = profile.friendRequests.all()
            plants = profile.plants.all()
        except Profile.DoesNotExist:
            context = {
                    "username": "Create a profile",
                    "first": "You may choose to enter your first name",
                    "last": "You may choose to enter your first name",
                    "bio": "You may choose to enter your bio",
                    "date": "You must be above the age of 16 to register for this site"}
            return render(request, "flights/profileCreate.html", context)

    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, "flights/login.html", {"message": None})
        context = {
            "users": None,
            "profile": profile,
            "requests": requests,
            "plants": plants
        }
        return render(request, "flights/index.html", context)
        
    if request.method == 'POST':
        username = request.POST["username"]
        context = {
            "users": User.objects.filter(username=username),
            "profile": profile,
            "requests": requests,
            "plants": plants
        }
        return render(request, "flights/index.html", context)


# Plants
def newPlant(request):
    if request.method == 'GET':
        return render(request, "flights/newPlant.html")
    if request.method == 'POST':
        name = request.POST["name"]
        about = request.POST["about"]
        plant = Plant(name=name, about=about)
        plant.save()
        try:    
            myprofile = Profile.objects.get(user_id=request.user.id)
            myprofile.plants.add(plant)        
            myprofile.save()
        except Profile.DoesNotExist:
            raise Http404("You haent made a profile yet.")
        
        return HttpResponseRedirect(reverse('index'))

def plantDisplay(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    isLonely = plant.posts.filter(title="I'm feeling lonely").exists()
    if isLonely:
        lonelypost = plant.posts.get(title="I'm feeling lonely")
        if lonelypost.comments.count() > 0:
            isLonely = False     
    score = plant.posts.count()
    displayScore = score*4.5
    context={
        "plant": plant,
        "posts": plant.posts.all(),
        "score": displayScore
    }
    
    if score > -1 and score < 3 and isLonely:
        return render(request, "flights/plant/plant1.html", context)
    if score > 2 and score < 5 and isLonely:
        return render(request, "flights/plant/angry1.html", context)
    if score > 4 and isLonely:
        return render(request, "flights/plant/angry2.html", context)
    if score > -1 and score < 3:
        return render(request, "flights/plant/plant1.html", context)
    if score > 2 and score < 5:
        return render(request, "flights/plant/plant2.html", context)
    if score > 4:
        return render(request, "flights/plant/plant3.html", context)

def newPost(request, plant_id):
    if request.method == 'GET':
        context={
        "plant": Plant.objects.get(id=plant_id),
        }
        return render(request, "flights/postCreate.html", context)
    if request.method == 'POST':
        title = request.POST["title"]
        text = request.POST["text"]
        post = Post(title=title, text=text)
        post.save()
        try:    
            plant = Plant.objects.get(id=plant_id)
            plant.posts.add(post)        
            plant.save()
        except Plant.DoesNotExist:
            raise Http404("You haven't made this plant yet.")
        
        return HttpResponseRedirect(reverse('plantDisplay', args =[plant_id] ))

def postDisplay(request, post_id):
    if request.method == 'GET':
        post = Post.objects.get(id=post_id)
        context={
            "post": post,
            "comments": post.comments.all()
        }
        return render(request, "flights/postDisplay.html", context)
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        text = request.POST["text"]
        # myprofile = Profile.objects.get(user_id=request.user.id)
        comment = Comment(text=text)
        comment.save()
        post.comments.add(comment)

        context={
            "post": post,
            "comments": post.comments.all()
        }
        return render(request, "flights/postDisplay.html", context)
    



    
    
    


# PROFILES AND USER_USER INTERACTION.

def accept(request, user_id):
    try:    
        myprofile = Profile.objects.get(user_id=request.user.id)
        friend = User.objects.get(id=user_id)
        myprofile.friends.add(friend)        
        myprofile.friendRequests.remove(friend)
        myprofile.save()
    except Profile.DoesNotExist:
        raise Http404("You haent made a profile yet.")
    context={
            "friend": friend
        }
    return render(request, "flights/accept.html", context)

def profile(request, user_id):    
    if request.method == 'POST':
        try:    
            profile = Profile.objects.get(user_id=user_id)
            user = User.objects.get(id=user_id)
            profile.friendRequests.add(request.user)
            profile.save()
        except Profile.DoesNotExist:
            raise Http404("This user hasn't made a profile yet.")
        context={
                "user": user,
                "requested": "requested"
            }
        return render(request, "flights/friendRequest.html", context)

    if request.method == 'GET':      
        try:
            profile = Profile.objects.get(user_id=user_id)
            friends = profile.friends.all()
            requests = profile.friendRequests.all()
            user = User.objects.get(id=user_id)
        except Profile.DoesNotExist:    
            raise Http404("This user hasn't made a profile yet.")

        if request.user in friends:
            context={
                "profile": profile,
                "plants": profile.plants.all()            
                }
            return render(request, "flights/profileDisplay.html", context)  
        elif request.user in requests:
            context={
                "user": user,
                "requested": "requested"
            }
            return render(request, "flights/friendRequest.html", context)
        else:
            context={
                "user": user,
                "notRequested": "not"
            }
            return render(request, "flights/friendRequest.html", context)

def myprofile(request):        
    if request.method == 'POST':
        firstName = request.POST["first"]
        lastName = request.POST["last"]
        bioData = request.POST["bio"]
        dob = request.POST["date"]
        profile = Profile(user=request.user, first=firstName, last=lastName, bio=bioData, birthdate=dob)
        profile.save()
        
        context={
                "profile": profile,
                "plants": profile.plants.all()            
                }
        return render(request, "flights/profileDisplay.html", context)  
    
    if request.method == 'GET':
        try:
            profile = Profile.objects.get(user_id=request.user.id)
        except Profile.DoesNotExist:
            context = {
                "username": "Create a profile",
                "first": "You may choose to enter your first name",
                "last": "You may choose to enter your first name",
                "bio": "You may choose to enter your bio",
                "date": "You must be above the age of 16 to register for this site"

            }
            return render(request, "flights/profileCreate.html", context)
        context={
                "profile": profile,
                "plants": profile.plants.all()            
                }
        return render(request, "flights/profileDisplay.html", context)  


# Auth

def register_view(request):
    if request.method == 'GET':
        return render(request, "flights/register.html", {"message":None})
    
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        
        try:
            user = User.objects.create_user(
                username = request.POST["username"],
                email = request.POST["email"],
                password = request.POST["password"])
            user.save()
        except IntegrityError:
            return render(request, "flights/register.html", {"message": "Username already exists"})
        

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "flights/register.html", {"message": "invalid credentials"})


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flights/login.html", {"message": "invalid credentials"})

def logout_view(request):
    logout(request)
    return render(request, "flights/logout.html", {"message": "Logged out"})

