from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import RegistrationForm
from .models import Profile
from recipes.models import Recipe

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    user_recipes = Recipe.objects.filter(author=request.user)
    
    paginator = Paginator(user_recipes, 3)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    
    return render(request, 'registration/profile.html', {'profile': profile, 'user_recipes': recipes})

def user_logout(request):
    logout(request)
    return redirect('home') 