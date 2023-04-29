from rest_framework import serializers
from datetime import date

from reviews.models import Category, Genre, Title, Review, Comment
from rest_framework.relations import SlugRelatedField 
from users.models import User

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError(
                'Нельзя указывать год, который больше текущего.'
            )
        return value




class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True
    )
    text = serializers.Field(required=True)
    score = serializers.Field(required=True)

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date'
        )
        # extra_kwargs = {'text': {'required': True}}


class CommentSerializer(serializers.ModelSerializer):
    # review = SlugRelatedField(
    #     slug_field='title', read_only=True
    # )
    author = SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
