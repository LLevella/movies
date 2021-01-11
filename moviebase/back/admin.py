from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Genre, Movie, Actor


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "url", "draft")
    list_filter = ("genres", "year")
    search_fields = ("title", "genres__name")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age")


admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
