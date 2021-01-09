from django.urls import path

from . import views

urlpatterns = [
    path("player/<int:pk>/", views.MovieDetailView.as_view()),
]