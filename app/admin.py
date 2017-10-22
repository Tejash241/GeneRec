# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserProfile)
admin.site.register(Movie)
admin.site.register(UserMovieMap)
admin.site.register(Song)
admin.site.register(UserSongMap)
admin.site.register(Puzzle)
