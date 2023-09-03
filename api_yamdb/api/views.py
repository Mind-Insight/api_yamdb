from typing import Any

from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import Avg, QuerySet
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import Token, RefreshToken
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from .serializers import (
    UserRegistrationSerializer,
    UserTokenSerializer,
    UserSerializer,
)
from constants import LENGTH_CODE
from users.models import User
from .serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
    CommentSerializers,
    ReviewSerializers,
)
from reviews.models import Title, Category, Genre, Review
from .mixins import CreateListDestroySearchViewSet
from .permissions import (
    IsAdminOrAnonymous,
    IsAuthorOrModeratorOrAdmin,
    IsAdminOrRoleIsAdmin
)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели отзывов."""
    serializer_class = ReviewSerializers
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdmin
    ]

    def get_title(self) -> Title:
        """Получаем произведение."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self) -> QuerySet:
        """Получаем отзывы для произведения."""
        return (
            self.get_title()
            .reviews.select_related("author")
            .order_by("-pub_date")
        )

    def perform_create(self, serializer: ReviewSerializers) -> None:
        """Создаем отзыв.Присваеваем текущего пользователя и произведение."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели комментариев."""
    serializer_class = CommentSerializers
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdmin
    ]

    def get_review(self) -> Review:
        """Получаем отзыв."""
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self) -> QuerySet:
        """Получаем комментарии для отзыва."""
        return (
            self.get_review()
            .comments.select_related("author")
            .order_by("-pub_date")
        )

    def perform_create(self, serializer: CommentSerializers) -> None:
        """Создаем комментарий.Присваеваем текущего пользователя и отзыв."""
        serializer.save(author=self.request.user, review=self.get_review())


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для работы с объектами модели Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('name', 'genre__slug', 'category__slug')
    filterset_fields = ('year', 'name')
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrAnonymous
    )

    def get_queryset(self) -> QuerySet:
        """Формирует и возвращает queryset."""
        queryset: QuerySet = super().get_queryset()
        genre_slug: str = self.request.query_params.get('genre')
        category_slug: str = self.request.query_params.get('category')
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset.order_by("-year").annotate(
            rating=Avg("reviews__score")
        )

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Запрещает использовать метод PUT."""
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)
        return super().update(request, *args, **kwargs)


class CategoryViewSet(CreateListDestroySearchViewSet):
    """Представление для работы с объектами модели Category."""
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('id', 'name')


class GenreViewSet(CreateListDestroySearchViewSet):
    """Представление для работы с объектами модели Genre."""
    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by('id', 'name')


class UserRegistrationView(generics.CreateAPIView):
    """Представление для регистрации пользователя."""
    serializer_class = UserRegistrationSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Создает пользователя и отправляет код подтверждения
        на указанный адрес электронной почты.
        """
        serializer: dict[str, str] = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()
        confirmation_code: str = get_random_string(length=LENGTH_CODE)
        cache.set(user.username, confirmation_code)
        self.send_confirmation_code(user.email, confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def send_confirmation_code(
        self, email: str, confirmation_code: str
    ) -> None:
        """Отправка кода подтверждения по электронной почте."""
        subject: str = 'Код подтверждения регистрации в YaMDB'
        message: str = f'Ваш код подтверждения: {confirmation_code}'
        from_email: str = 'yamdb@gmail.com'
        recipient_list: list[str] = [email]
        send_mail(subject, message, from_email, recipient_list)


class UserTokenView(generics.CreateAPIView):
    """Получение пользователем JWT-токена."""
    serializer_class = UserTokenSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Обработка POST-запроса на получение JWT-токена."""
        serializer: dict[str, str] = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username: str = request.data['username']
        user: User = get_object_or_404(User, username=username)
        refresh: Token = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)})


class UserViewSet(viewsets.ModelViewSet):
    """ Представление для работы с пользователями в системе."""
    serializer_class = UserSerializer
    queryset = User.objects.order_by('username').all()
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthenticated, IsAdminOrRoleIsAdmin]
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request: Request) -> Response:
        """Получает информацию о текущем пользователе."""
        if request.method == 'PATCH':
            serializer: UserSerializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer: UserSerializer = self.get_serializer(request.user)
        return Response(serializer.data)