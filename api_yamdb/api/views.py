from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import FROM_EMAIL
from reviews.models import Category, Genre, Title, Review
from users.models import User
from .filters import TitleFilter
from .permissions import (
    IsAdmin, IsAdminOrReadOnly,
    IsAdminOrModeratorOrAuthorOrReadOnly)
from .serializers import (
    CategorySerializer, GenreSerializer, TitlePostSerializer,
    TitleGetSerializer, ReviewSerializer, CommentSerializer,
    UserSerializer, TokenSerializer, RegisterUserSerializer,
    UserEditSerializer
)


class CategoryViewSet(ListModelMixin,
                      CreateModelMixin,
                      DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    Получение списка всех категорий, категории по id,
    создание/удаление категории по id.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'


class GenreViewSet(ListModelMixin,
                   CreateModelMixin,
                   DestroyModelMixin,
                   viewsets.GenericViewSet
                   ):
    """
    Получение списка всех жанров, жанра по id,
    создание/удаление жанра по id.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """
    Получение всех тайтлов, тайтла по id,
    создание/обновление/частичное обновление/удаление тайтла по id.
    """
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = TitleFilter
    search_fields = ('category__slug', 'genre__slug', 'name', 'year',)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleGetSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Получение всех отзывов, отзыва по id,
    создание/обновление/частичное обновление/удаление отзыва по id.
    """
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrModeratorOrAuthorOrReadOnly]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

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
    permission_classes = [IsAdminOrModeratorOrAuthorOrReadOnly]
    pagination_class = PageNumberPagination

    def get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comment.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=self.get_review())


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    Функция регистрации нового пользователя и отправки кода
    подтверждения на email.
    """
    serializer = RegisterUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email')
        )
    except IntegrityError:
        return Response('Пользователь с таким именем/почтой уже существует',
                        status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация YAMDB',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=FROM_EMAIL,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """
    Функция генерации и валидации JWT-Токена.
    """
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )

    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех польваотелей, пользователя по id,
    создание/частичное обновление/удаление объекта пользователя по id.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    http_method_names = ('get', 'post', 'patch', 'delete',)
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email']
    permission_classes = (IsAdmin,)

    @action(
        methods=['get', 'patch', ],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
