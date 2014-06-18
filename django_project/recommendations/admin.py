from django.contrib import admin

from .models import Movie, Preferences, MovieRecom

admin.site.register(Movie)
admin.site.register(MovieRecom)
admin.site.register(Preferences)