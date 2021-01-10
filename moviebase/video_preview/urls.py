from django.urls import path

from . import views

urlpatterns = [
    path("<slug:slug>/", views.MovieDetailView.as_view()),
]