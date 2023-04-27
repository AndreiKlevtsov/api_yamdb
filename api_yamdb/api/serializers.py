from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Review, Comment
from users.models import User


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
