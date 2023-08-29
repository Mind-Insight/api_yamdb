from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Title, Genre, GenreTitle


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    # TODO: title rating
    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    def create(self, validated_data):
        genres = validated_data.pop("genre")
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre, _ = Genre.objects.get_or_create(**genre)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title
