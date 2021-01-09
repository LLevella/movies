from rest_framework import serializers
from .models import MoviePlayer


class MovieDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    # directors = ActorListSerializer(read_only=True, many=True)
    # actors = ActorListSerializer(read_only=True, many=True)
    # genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)

    class Meta:
        model = MoviePlayer
        exclude = ("draft",)