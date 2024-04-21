from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.


def loginUser(request):

    if request.user.is_authenticated: #if i access login page after authentication , redirected to profiles
        return redirect('profiles')


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username) #checks if username exist
        except:
            messages.error(request,'Username does not exist')    

        user = authenticate(request, username=username, password=password) # makes sure password matches username and returns that specific user

        if user is not None:
            login(request, user) # login function creates a session for the user in the DB and gets that session and adds it to browser cookies
            return redirect('profiles')
        else:
            messages.error(request,'Username OR Password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.error(request,'User was logged out')
    return redirect('login')


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html',context)


def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    
    topSkills = profile.skill_set.exclude(description__exact="") # filters skills with no description
    otherSkills = profile.skill_set.filter(description="") # give skills with empty description



    context={'profile': profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request,'users/user-profile.html',context)