from rest_framework import serializers
from datetime import date

from reviews.models import Category, Genre, Title, Review, Comment
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from users.models import User



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)

    def validate_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError(
                'Нельзя указывать год, который больше текущего.'
            )
        return value


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.DecimalField(max_digits=3, decimal_places=2,
                                      read_only=True)

    class Meta:
        model = Title
        fields = (
        'id', 'name', 'year', 'rating', 'description', 'genre', 'category',)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале')
        return value

    # def validate(self, data):
    #     request = self.context['request']
    #     author = request.user
    #     title_id = self.context.get('view').kwargs.get('title_id')
    #     title = get_object_or_404(Title, pk=title_id)
    #     if (
    #             request.method == 'POST'
    #             and Review.objects.filter(title=title, author=author).exists()
    #     ):
    #         raise ValidationError('Такой отзыв уже создан')
    #     return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
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


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
