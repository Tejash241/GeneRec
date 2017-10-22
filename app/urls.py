from django.conf.urls import url
from . import views

urlpatterns = [

    # url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^movies/', views.movies, name='movies'),
    url(r'^music/', views.music, name='music'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^authenticate/', views.authenticate, name='authenticate'),
    url(r'^callback/', views.callback, name='callback'),
    url(r'^mind/', views.mind, name='mind'),
    url(r'^books/', views.books, name='books'),
]
