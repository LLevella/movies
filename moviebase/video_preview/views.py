from django.db import models
from rest_framework import generics, permissions, viewsets
from .models import MoviePlayer
from .serializers import MovieDetailSerializer

class MovieDetailView(generics.RetrieveAPIView):
    """Вывод фильма"""
    queryset = MoviePlayer.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer
    permission_classes = [permissions.IsAuthenticated]