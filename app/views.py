# -*- coding: utf-8 -*-
from django.shortcuts import *
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import *
from django.contrib import messages


# Create your views here.

def index(request):
    context = {}
    return render(request, 'app/index.html', context)


def movies(request):
    context = {}
    return render(request, 'app/movies.html', context)


def music(request):
    context = {}
    return render(request, 'app/music.html', context)


def login(request):
    if request.session.get('user_id', None) is not None:
        return redirect('index')

    if request.method == "POST":
        email = request.POST.get("user_id")
        password = request.POST.get("password")
        if UserProfile.objects.filter(user_id=email, password=password).exists():
            request.session['user_id'] = email
            request.session['password'] = password
            return redirect('index')
        else:
            messages.error(request, 'No matching User exists.')
            return redirect('login')
    else:
        context = {}
        return render(request, 'app/login.html', context)


def register(request):
    if request.session.get('user_id', None) is not None:
        return redirect('index')
    if request.method == "POST":
        email = request.POST.get("user_id")
        password = request.POST.get("password")
        if UserProfile.objects.filter(user_id=email).exists():
            messages.error(request, 'User with same User ID already exists.')
            return redirect('register')
        else:
            user = UserProfile(user_id=email, password=password)
            user.save()
            messages.success(request, 'You have successfully registered. Please Login now!')
            return redirect('login')
    else:
        context = {}
        return render(request, 'app/register.html', context)


def logout(request):
    del request.session['user_id']
    context = {}
    return redirect('login')
