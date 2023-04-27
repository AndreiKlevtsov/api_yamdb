from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Review, Comment, Title
from users.models import User

from api.serializers import (
    ReviewSerializer, CommentSerializer, UserSerializer
)


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

    #
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
