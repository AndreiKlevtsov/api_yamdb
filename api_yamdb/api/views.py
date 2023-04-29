from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from reviews.models import Category, Genre, Title, Review, Comment, Title

from .serializers import (
    CategorySerializer, GenreSerializer, TitlePostSerializer,
    TitleGetSerializer,
    ReviewSerializer, CommentSerializer, UserSerializer)

from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from users.models import User


class CategoryViewSet(ListModelMixin,
                      CreateModelMixin,
                      DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListModelMixin,
                   CreateModelMixin,
                   DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category__slug', 'genre__slug', 'name', 'year',)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitlePostSerializer
        return TitleGetSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Получение всех отзывов, отзыва по id,
    создание/обновление/частичное обновление/удаление отзыва по id.
    """
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_title(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получение всех комментариев, комментария к отзыву по id,
    создание/обновление/частичное обновление/удаление комментария по id.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_review(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review

    def get_queryset(self):
        return self.get_review().comment.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email']
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def me(self):
        pass
