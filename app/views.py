# -*- coding: utf-8 -*-
from django.shortcuts import *
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import *
from django.contrib import messages
from random import shuffle
from functions import *
from recommender import *
from youtube_api import *
import genomelink
import os


# Create your views here.

def index(request):
    if request.session.get('user_id', None) is None:
        return redirect('login')
    current_user_id = request.session['user_id']
    if UserProfile.objects.get(user_id=current_user_id).authenticated == 0:
        link = get_auth_url()
        context = {'not_registered': True, 'link': link}

        return render(request, 'app/index.html', context)

    current_cluster = UserProfile.objects.get(user_id=current_user_id).cluster_name

    user = UserProfile.objects.get(user_id=current_user_id)
    context = {'cid': current_cluster, 'not_registered': False, 'user': user}
    return render(request, 'app/index.html', context)


def books(request):
    if request.session.get('user_id', None) is None:
        return redirect('login')
    current_user_id = request.session['user_id']
    current_cluster = UserProfile.objects.get(user_id=current_user_id).cluster_name
    other_users_in_cluster = UserProfile.objects.filter(cluster_name=current_cluster)
    probable_books = set()

    for user in other_users_in_cluster:
        uid = user.user_id
        user_books = UserBookMap.objects.filter(user=user)
        for book in user_books:
            probable_books.add(book.book)

    probable_books = list(probable_books)
    shuffle(probable_books)
    probable_books = probable_books[0:min(4, len(probable_books) - 1)]

    mov = []

    for m in probable_books:
        url = get_google_book(m.isbn)
        m.url = url
        mov.append(m)

    context = {'books': mov}
    return render(request, 'app/books.html', context)


def movies(request):
    if request.session.get('user_id', None) is None:
        return redirect('login')
    current_user_id = request.session['user_id']
    current_cluster = UserProfile.objects.get(user_id=current_user_id).cluster_name
    other_users_in_cluster = UserProfile.objects.filter(cluster_name=current_cluster)
    probable_movies = set()

    for user in other_users_in_cluster:
        uid = user.user_id
        user_movies = UserMovieMap.objects.filter(user=user)
        for movie in user_movies:
            if movie.rating >= 4:
                probable_movies.add(movie.movie)

    probable_movies = list(probable_movies)
    shuffle(probable_movies)
    probable_movies = probable_movies[0:min(200, len(probable_movies) - 1)]

    mov = []
    total = 0
    for m in probable_movies:
        if int(m.vote_average) > 6.5 and total < 4:
            img = get_movie_details(m.title)
            # img = 'sdf'
            if img is not None:
                m.cover = img
                mov.append(m)
                total += 1

    context = {'movies': mov}
    return render(request, 'app/movies.html', context)


def music(request):
    if request.session.get('user_id', None) is None:
        return redirect('login')
    current_user_id = request.session['user_id']
    current_cluster = UserProfile.objects.get(user_id=current_user_id).cluster_name
    other_users_in_cluster = UserProfile.objects.filter(cluster_name=current_cluster)
    probable_songs = set()

    for user in other_users_in_cluster:
        uid = user.user_id
        user_songs = UserSongMap.objects.filter(user=user)
        print len(user_songs)
        for song in user_songs:
            probable_songs.add(song.song)

    probable_songs = list(probable_songs)
    shuffle(probable_songs)
    probable_songs = probable_songs[0:min(4, len(probable_songs) - 1)]
    print probable_songs
    mov = []
    for m in probable_songs:
        url = get_youtube_video(m.artist + "-" + m.name)

        if url is not None:
            link = 'https://www.youtube.com/embed/' + url
            m.link = link
            mov.append(m)

    context = {'music': mov}
    return render(request, 'app/music.html', context)


def mind(request):
    if request.session.get('user_id', None) is None:
        return redirect('login')
    current_user_id = request.session['user_id']
    user = UserProfile.objects.get(user_id=current_user_id)
    if user.childhood_intelligence is None:
        intel = 3
    else:
        intel = int(user.childhood_intelligence)
    puzzle = Puzzle.objects.filter(difficulty=intel)[0]

    context = {'puzzle': puzzle}
    return render(request, 'app/mind.html', context)


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


def callback(request):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # The user has been redirected back from the provider to your registered
    # callback URL. With this redirection comes an authorization code included
    # in the request URL. We will use that to obtain an access token.
    token = genomelink.OAuth.token(client_id='KyoEsiyBMGDj78a0H197DOA53T9013K8m3zrYs4a',
                                   client_secret='3tEk4tca6LImP4yfkjUdqcgkBBTSFNe1hdnNh4PAtj9AagdSSKqJzJKKqoXUJRoBgICEKmw9JbCsmu5dnw3ozOzK5PF3ZT1OSfNKjIgelm5dujKAoHcOxh8zSYXbwFXL',
                                   callback_url='http://127.0.0.1:8000/app/callback',
                                   request_url=request.get_full_path())

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token in index page.

    request.session['oauth_token'] = token
    reports = []
    if 'oauth_token' in request.session:
        for name in ['agreeableness', 'neuroticism', 'extraversion', 'conscientiousness', 'openness', 'anger',
                     'reward-dependence', 'harm-avoidance', 'gambling', 'novelty-seeking']:
            reports.append(
                genomelink.Report.fetch(name=name, population='european', token=request.session['oauth_token']))

    report_data = dict()
    for report in reports:
        if report.summary['score'] is not None:
            report_data[report.phenotype['display_name']] = int(report.summary['score'])
    print report_data

    user = UserProfile.objects.get(user_id=request.session['user_id'])
    user.authenticated = 1
    for attr, value in report_data.iteritems():
        attr = attr.lower()
        attr = attr.replace('-', '_')
        attr = attr.replace(' ', '_')
        setattr(user, attr, value)
        user.authenticated = 1
    user.save()

    assign_cluster_to_newuser(user)

    return redirect('index')


def authenticate(request):
    url = get_auth_url()
    print url
    return redirect('index')
